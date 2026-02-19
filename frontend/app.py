import streamlit as st
import requests

# API Configuration
API_V1_STR = "http://localhost:8000/api/v1"
RECOMMENDER_URL = f"{API_V1_STR}/recommender"
TMDB_URL = f"{API_V1_STR}/tmdb"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System")

# Initialize session state for selection
if 'selected_movie_name' not in st.session_state:
    st.session_state.selected_movie_name = None

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

def set_movie(movie_title):
    st.session_state.selected_movie_name = movie_title

# Helper to fetch data
@st.cache_data(ttl=60)
def fetch_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

# Helper to display a row of movies
def display_movie_row(title, movies):
    st.markdown(f"### {title}")
    if not movies:
        st.info("No movies found.")
        return

    cols = st.columns([1, 4, 4, 4, 4, 4, 1])
    # We use indices 1-5 for the 5 movies to center them
    for i in range(min(len(movies), 5)):
        movie = movies[i]
        with cols[i+1]:
            st.image(movie['poster'], use_container_width=True)
            st.button(movie['title'], key=f"btn_{title}_{movie['id']}", on_click=set_movie, args=(movie['title'],))



# --- Hero Section ---
trending = fetch_from_api(f"{TMDB_URL}/trending")
now_playing = fetch_from_api(f"{TMDB_URL}/now-playing")
popular_tv = fetch_from_api(f"{TMDB_URL}/popular-tv")
top_rated = fetch_from_api(f"{TMDB_URL}/top-rated")
upcoming = fetch_from_api(f"{TMDB_URL}/upcoming")



# --- Search Section ---
st.markdown("## 🔍 Search")

# Fetch movie list with searchable tags
movie_choices = fetch_from_api(f"{RECOMMENDER_URL}/movies")

# Determine default index
default_index = None
GENRES_LIST = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Sci-Fi", "TV Movie", "Thriller", "War", "Western"]

if st.session_state.selected_movie_name:
    # Try to find the matching option
    try:
        default_index = movie_choices.index(st.session_state.selected_movie_name)
    except ValueError:
        default_index = None

selected_movie_raw = st.selectbox(
    "Search for a movie or genre (real-time filtering)",
    movie_choices if movie_choices else [],
    index=default_index,
    placeholder="Type to search...",
    key="search_box"
)

if selected_movie_raw:
    val = selected_movie_raw
    # Update session state if changed
    if val != st.session_state.selected_movie_name:
        st.session_state.selected_movie_name = val
        st.rerun()

# Use session state as the source of truth
selected_movie = st.session_state.selected_movie_name

if selected_movie:
    if selected_movie in GENRES_LIST:
        st.subheader(f"📂 Genre: {selected_movie}")
        with st.spinner(f"Finding movies in {selected_movie}..."):
             results = fetch_from_api(f"{RECOMMENDER_URL}/search?q={selected_movie}")
             if results:
                 st.write(f"Found {len(results)} matching movies:")
                 cols = st.columns(5)
                 for i, title in enumerate(results):
                     with cols[i % 5]:
                         if st.button(title, key=f"genre_res_{i}", use_container_width=True):
                             set_movie(title)
                             st.rerun()
             else:
                 st.info("No movies found for this genre.")
                 
    else:
        with st.spinner(f"Finding recommendations for '{selected_movie}'..."):
            try:
                response = requests.post(f"{RECOMMENDER_URL}/recommend", json={"movie_title": selected_movie})
                response.raise_for_status()
                data = response.json()
            
                if data:
                    recommendations = data.get("recommendations", [])
                    
                    # Movie Details Section
                    source_movie = data.get("source_movie")
                    if source_movie:
                        col1, col2, col3 = st.columns([1, 2, 4])
                        
                        with col2:
                            if source_movie.get('poster'):
                                st.image(source_movie['poster'], use_container_width=True)
                                
                        with col3:
                            st.subheader(source_movie.get('title'))
                            st.write(f"**Rating:** ⭐ {source_movie.get('rating', 0)}/10")
                            
                            # Metadata Row
                            meta_cols = st.columns([1, 1])
                            with meta_cols[0]:
                                if source_movie.get('release_date'):
                                    st.write(f"📅 **Date:** {source_movie.get('release_date')}")
                            with meta_cols[1]:
                                if source_movie.get('runtime'):
                                    st.write(f"⏱️ **Time:** {source_movie.get('runtime')} min")
                                    
                            if source_movie.get('genres'):
                                st.write(f"🎭 **Genres:** {', '.join(source_movie.get('genres'))}")
                            
                            if source_movie.get('director'):
                                st.write(f"🎬 **Director:** {source_movie.get('director')}")
                                
                            if source_movie.get('cast'):
                                st.write(f"👥 **Cast:** {', '.join(source_movie.get('cast'))}")
                                
                            st.write(f"📝 **Overview:** {source_movie.get('overview')}")
                            
                            if source_movie.get('imdb_id'):
                                imdb_url = f"https://www.imdb.com/title/{source_movie.get('imdb_id')}"
                                st.link_button("Learn more on IMDb ↗", imdb_url)
                    
                    if recommendations:
                        st.markdown("---")
                        st.subheader(f"Because you selected *{selected_movie}*")
                        
                        # Row 1 (Top 5)
                        cols = st.columns([1, 4, 4, 4, 4, 4, 1])
                        for i in range(min(5, len(recommendations))):
                            movie = recommendations[i]
                            with cols[i+1]:
                                st.image(movie.get('poster'), use_container_width=True)
                                st.button(movie.get('title'), key=f"rec_1_{i}", on_click=set_movie, args=(movie.get('title'),))
                                if movie.get('reasoning'):
                                    st.markdown(f"<div style='font-size: 0.8em; color: #888;'>{movie.get('reasoning')}</div>", unsafe_allow_html=True)
                        
                        # Row 2 (Next 5)
                        if len(recommendations) > 5:
                            st.markdown("<br>", unsafe_allow_html=True)
                            cols2 = st.columns([1, 4, 4, 4, 4, 4, 1])
                            for i in range(5, min(10, len(recommendations))):
                                movie = recommendations[i]
                                with cols2[i-5+1]:
                                    st.image(movie.get('poster'), use_container_width=True)
                                    st.button(movie.get('title'), key=f"rec_2_{i}", on_click=set_movie, args=(movie.get('title'),))
                                    if movie.get('reasoning'):
                                        st.markdown(f"<div style='font-size: 0.8em; color: #888;'>{movie.get('reasoning')}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error getting recommendations: {e}")

st.markdown("---")


display_movie_row("🔥 Trending Today", trending)
display_movie_row("🎥 Now Playing in Theaters", now_playing)
display_movie_row("📺 Popular TV Series", popular_tv)
display_movie_row("⭐ Top Rated Movies", top_rated)
display_movie_row("📅 Upcoming Releases", upcoming)
