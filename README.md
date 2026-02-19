# Movie and Web-Series Recommender System

A full-stack movie recommendation application using **FastAPI** for the backend and **Streamlit** for the frontend. It provides personalized movie recommendations based on content similarity and displays trending/popular movies using the TMDB API.

## 🚀 Features

- **Movie Web-Series Recommendations**: Content-based filtering to suggest similar movies and web-series.
- **Search**: Search for movies and web-series or filter by genre.
- **Trending & Popular**: View trending, now playing, top-rated, and upcoming movies.
- **Interactive UI**: Clean and responsive interface built with Streamlit.
- **API Documentation**: Auto-generated Swagger UI for the backend.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit
- **ML/Data**: Scikit-Learn, Pandas, Pickle
- **External API**: The Movie Database (TMDB) API

## 📂 Project Structure

```bash
Movie-Recommender-System/
├── backend/
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── services/       # Business logic
│   │   └── main.py         # App entry point
│   └── model/              # ML models (pickled files)
├── frontend/
│   └── app.py              # Streamlit application
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## ⚙️ Setup & Installation

1.  **Clone the repository** (if applicable):
    ```bash
    git clone <repository-url>
    cd Movie-Recommender-System
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Create a `.env` file in the root directory and add your TMDB API Key:
    ```env
    API_KEY=your_tmdb_api_key_here
    ```

## 🏃‍♂️ Running the Application

You need to run both the backend and frontend terminals.

### 1. Start the Backend server

In a new terminal:
```bash
# From the root directory (Movie-Recommender-System)
python -m backend.app.main
# OR
uvicorn backend.app.main:app --reload
```
The API will be available at `http://localhost:8000`.
API Docs: `http://localhost:8000/docs`

### 2. Start the Frontend app

In a separate terminal:
```bash
# From the root directory (Movie-Recommender-System)
streamlit run frontend/app.py
```
The app will open in your browser at `http://localhost:8501`.

## ⚠️ Large Files Note

The `backend/model/similarity.pkl` file is large (~184MB) and is excluded from Git tracking to comply with GitHub file size limits.

If you are setting this up from scratch, you will need to ensure this file exists in `backend/model/` or use Git LFS to track it if you have it.
