
import requests
from typing import List, Optional, Tuple
from backend.app.core.config import settings
from backend.app.schemas.schemas import MovieSchema

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    def fetch_from_tmdb(self, endpoint: str) -> List[MovieSchema]:
        if not settings.API_KEY:
            return []
            
        url = f"{self.BASE_URL}{endpoint}?api_key={settings.API_KEY}&language=en-US"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("results", [])[:10]: # Limit to top 10 for performance
                poster_path = item.get("poster_path")
                poster_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
                
                backdrop_path = item.get("backdrop_path")
                backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

                title = item.get("title") or item.get("name")
                release_date = item.get("release_date") or item.get("first_air_date")
                
                results.append(MovieSchema(
                    id=item.get("id"),
                    title=title,
                    poster=poster_url,
                    backdrop=backdrop_url,
                    overview=item.get("overview", ""),
                    rating=item.get("vote_average", 0.0),
                    release_date=release_date
                ))
            return results
        except Exception as e:
            print(f"Error fetching data from TMDB endpoint {endpoint}: {e}")
            return []
    
    def search_movie(self, query: str) -> List[MovieSchema]:
        """Search for a movie by title"""
        if not settings.API_KEY:
             return []
        
        url = f"{self.BASE_URL}/search/movie?api_key={settings.API_KEY}&language=en-US&query={query}&page=1"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("results", [])[:1]: # Get top match
                 poster_path = item.get("poster_path")
                 poster_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
                 
                 backdrop_path = item.get("backdrop_path")
                 backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

                 results.append(MovieSchema(
                    id=item.get("id"),
                    title=item.get("title"),
                    poster=poster_url,
                    backdrop=backdrop_url,
                    overview=item.get("overview", ""),
                    rating=item.get("vote_average", 0.0),
                    release_date=item.get("release_date")
                ))
            return results
        except Exception as e:
            print(f"Error searching TMDB for {query}: {e}")
            return []

    def get_recommendations(self, movie_id: int) -> List[MovieSchema]:
        """Get recommendations for a specific movie ID"""
        return self.fetch_from_tmdb(f"/movie/{movie_id}/recommendations")

    def get_similar_movies(self, movie_id: int) -> List[MovieSchema]:
        """Get similar movies for a specific movie ID (fallback for recommendations)"""
        return self.fetch_from_tmdb(f"/movie/{movie_id}/similar")

    def get_movie_details(self, movie_id: int) -> Optional[MovieSchema]:
        """Get full details for a movie by ID"""
        if not settings.API_KEY:
            return None
            
        url = f"{self.BASE_URL}/movie/{movie_id}?api_key={settings.API_KEY}&language=en-US&append_to_response=credits,keywords"
        try:
            response = requests.get(url)
            response.raise_for_status()
            item = response.json()
            
            poster_path = item.get("poster_path")
            poster_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
            
            backdrop_path = item.get("backdrop_path")
            backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

            title = item.get("title") or item.get("name")
            release_date = item.get("release_date") or item.get("first_air_date")
            
            # Extract credits
            credits = item.get("credits", {})
            cast = [c.get("name") for c in credits.get("cast", [])[:5]] # Top 5 cast
            director = next((c.get("name") for c in credits.get("crew", []) if c.get("job") == "Director"), None)
            
            # Extract keywords
            keywords = [k.get("name") for k in item.get("keywords", {}).get("keywords", [])]
            
            return MovieSchema(
                id=item.get("id"),
                title=title,
                poster=poster_url,
                backdrop=backdrop_url,
                overview=item.get("overview", ""),
                rating=item.get("vote_average", 0.0),
                release_date=release_date,
                genres=[g.get("name") for g in item.get("genres", [])],
                vote_count=item.get("vote_count", 0),
                runtime=item.get("runtime"),
                director=director,
                cast=cast,
                keywords=keywords,
                imdb_id=item.get("imdb_id")
            )
        except Exception as e:
            print(f"Error fetching movie details for {movie_id}: {e}")
            return None

    def get_trending(self) -> List[MovieSchema]:
        return self.fetch_from_tmdb("/trending/all/day")

    def get_now_playing(self) -> List[MovieSchema]:
        return self.fetch_from_tmdb("/movie/now_playing")

    def get_popular_tv(self) -> List[MovieSchema]:
        return self.fetch_from_tmdb("/tv/popular")

    def get_top_rated(self) -> List[MovieSchema]:
        return self.fetch_from_tmdb("/movie/top_rated")

    def get_upcoming(self) -> List[MovieSchema]:
        return self.fetch_from_tmdb("/movie/upcoming")

tmdb_service = TMDBService()
