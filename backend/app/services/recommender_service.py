
import pickle
import requests
import pandas as pd
import difflib
from backend.app.core.config import settings
from backend.app.services.tmdb_service import tmdb_service
from backend.app.schemas.schemas import MovieSchema

class RecommenderService:
    def __init__(self):
        try:
            self.movies = pickle.load(open(settings.MOVIES_PKL, 'rb'))
            self.similarity = pickle.load(open(settings.SIMILARITY_PKL, 'rb'))
        except FileNotFoundError:
            print(f"Model files not found at {settings.MODEL_PATH}")
            self.movies = None
            self.similarity = None

    def get_movie_titles(self):
        import re
        GENRES_LIST = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Sci-Fi", "TV Movie", "Thriller", "War", "Western"]
        
        local_movies = []
        if self.movies is not None:
             for _, row in self.movies.iterrows():
                 local_movies.append(row['title'])
        
        # Add trending and popular titles from TMDB to the list
        try:
             tmdb_movies = []
             trending = tmdb_service.get_trending()
             now_playing = tmdb_service.get_now_playing()
             upcoming = tmdb_service.get_upcoming()
             
             for m in trending + now_playing + upcoming:
                 if m.title:
                     tmdb_movies.append(m.title)
             
             # Combine locally, add Genres, and deduplicate
             all_movies = sorted(list(set(local_movies + tmdb_movies + GENRES_LIST)))
             return all_movies
        except Exception:
             return sorted(list(set(local_movies + GENRES_LIST)))

    def fetch_poster(self, movie_id):
        if not settings.API_KEY:
            return "https://via.placeholder.com/500x750?text=No+API+Key"
        
        try:
            url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, settings.API_KEY)
            response = requests.get(url)
            data = response.json()
            poster_path = data.get('poster_path')
            
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster"
        except Exception as e:
            print(f"Error fetching poster for movie {movie_id}: {e}")
            return "https://via.placeholder.com/500x750?text=Error"

    def find_closest_movie(self, title: str):
        if self.movies is None:
            return None
        
        # 1. Exact match
        if title in self.movies['title'].values:
            return title
            
        # 2. Case-insensitive match normalization
        # Create a mapping of lower_case -> real_title
        title_map = {t.lower(): t for t in self.movies['title'].values}
        
        if title.lower() in title_map:
            return title_map[title.lower()]
            
        # 3. Very Close Match (Typo tolerance only)
        # We increase cutoff to 0.85 to avoid matching "The Avengers" to "Avengers: Infinity War" or unrelated movies
        matches = difflib.get_close_matches(title, self.movies['title'].values, n=1, cutoff=0.85)
        if matches:
            return matches[0]
            
        return None

    def generate_reasoning(self, source: MovieSchema, target: MovieSchema):
        reasons = []
        
        # Genres
        s_genres = set(source.genres) if source.genres else set()
        t_genres = set(target.genres) if target.genres else set()
        common_genres = list(s_genres & t_genres)
        if common_genres:
            reasons.append(f"Genre: {', '.join(common_genres[:2])}")
            
        # Keywords
        s_keywords = set(source.keywords) if source.keywords else set()
        t_keywords = set(target.keywords) if target.keywords else set()
        common_keywords = list(s_keywords & t_keywords)
        if common_keywords:
            reasons.append(f"Keywords: {', '.join(common_keywords[:2])}")
            
        # Director
        if source.director and target.director and source.director == target.director:
            reasons.append(f"Director: {source.director}")
            
        # Cast
        s_cast = set(source.cast) if source.cast else set()
        t_cast = set(target.cast) if target.cast else set()
        common_cast = list(s_cast & t_cast)
        if common_cast:
            reasons.append(f"Cast: {', '.join(common_cast[:2])}")
            
        if not reasons:
             return "Recommended based on similar themes and style."
             
        return "Recommended because it shares: " + " | ".join(reasons)

    def search_movies(self, query: str):
        """Search for movies by title or genre/tag in local database"""
        results = []
        if self.movies is not None:
             # Search in Title OR Tags (Genre usually in tags)
             mask = (
                 self.movies['title'].str.contains(query, case=False, na=False) | 
                 self.movies['tags'].str.contains(query, case=False, na=False)
             )
             matches = self.movies[mask]
             results = matches['title'].head(20).tolist()
        
        # If few local results, maybe search TMDB? 
        # For now, let's mix the filtered results with the full list if query is empty, but we are searching query.
        return results

    def recommend(self, movie_title: str):
        recommendations = []
        source_movie = None
        
        # 1. Try Local Content-Based Filtering
        local_title = self.find_closest_movie(movie_title)
        
        if local_title:
            print(f"Movie '{movie_title}' resolved to local model title '{local_title}'")
            try:
                movie_index = self.movies[self.movies['title'] == local_title].index[0]
                distances = self.similarity[movie_index]
                movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

                for i in movies_list:
                    movie_id = self.movies.iloc[i[0]].movie_id
                    
                    # Fetch full details for the recommended movie
                    details = tmdb_service.get_movie_details(int(movie_id))
                    if details:
                        recommendations.append(details)
                    else:
                        # Fallback if details fail
                        poster = self.fetch_poster(movie_id)
                        recommendations.append(MovieSchema(
                            id=int(movie_id),
                            title=self.movies.iloc[i[0]].title,
                            poster=poster,
                            rating=0.0
                        ))
                    
                # Also return the source movie details
                source_movie_id = self.movies.iloc[movie_index].movie_id
                source_movie = tmdb_service.get_movie_details(int(source_movie_id))
                
                if not source_movie:
                    # Fallback
                    poster = self.fetch_poster(source_movie_id)
                    source_movie = MovieSchema(
                        id=int(source_movie_id), 
                        title=local_title, 
                        poster=poster, 
                        rating=0.0
                    )
            except Exception as e:
                print(f"Local recommendation error: {e}")
        
        # 2. Fallback to TMDB Logic if not found locally or error occurred
        if not recommendations:
            print(f"Movie '{movie_title}' not found locally or local failed. Searching TMDB...")
            search_results = tmdb_service.search_movie(movie_title)
            
            if search_results:
                 # Fetch full details for source movie
                 source_movie_light = search_results[0]
                 source_movie = tmdb_service.get_movie_details(source_movie_light.id)
                 if not source_movie:
                     source_movie = source_movie_light
                 
                 recs_light = tmdb_service.get_recommendations(source_movie.id) 
                 
                 if not recs_light:
                     print(f"No recommendations found for '{movie_title}' from TMDB. Trying similar movies...")
                     recs_light = tmdb_service.get_similar_movies(source_movie.id)
                 
                 # Enrich recommendations
                 for rec in recs_light[:10]:
                     details = tmdb_service.get_movie_details(rec.id)
                     if details:
                         recommendations.append(details)
                     else:
                         recommendations.append(rec)
        
        # 3. Compute Reasoning
        if source_movie and recommendations:
            for rec in recommendations:
                rec.reasoning = self.generate_reasoning(source_movie, rec)
                
        return recommendations, source_movie

recommender_service = RecommenderService()
