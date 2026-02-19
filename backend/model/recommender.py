import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(current_dir, '..', '..', '.env'))

API_KEY = os.getenv("API_KEY")

movies_path = os.path.join(current_dir, 'movies.pkl')
similarity_path = os.path.join(current_dir, 'similarity.pkl')

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/500x750?text=No+API+Key"
    
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, API_KEY)
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

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommended_movies = []
    recommended_movies_posters = []        

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters
