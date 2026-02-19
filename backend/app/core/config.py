import os
from dotenv import load_dotenv


# Calculate project root from config file location: backend/app/core/config.py -> ../../../.. -> root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

class Settings:
    PROJECT_NAME: str = "Movie Recommender System"
    API_V1_STR: str = "/api/v1"
    API_KEY: str = os.getenv("API_KEY")
    
    # Path to the model files
    BASE_DIR = ROOT_DIR
    MODEL_PATH = os.path.join(BASE_DIR, "backend", "model")
    MOVIES_PKL = os.path.join(MODEL_PATH, "movies.pkl")
    SIMILARITY_PKL = os.path.join(MODEL_PATH, "similarity.pkl")

settings = Settings()
