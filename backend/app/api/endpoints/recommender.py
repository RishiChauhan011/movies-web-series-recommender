from fastapi import APIRouter
from backend.app.schemas.schemas import RecommendationRequest, RecommendationResponse
from backend.app.services.recommender_service import recommender_service
from typing import List

router = APIRouter()

@router.get("/movies", response_model=List[str])
def get_movies():
    return recommender_service.get_movie_titles()

@router.get("/search", response_model=List[str])
def search_movies(q: str = ""):
    return recommender_service.search_movies(q)

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    recommendations, source_movie = recommender_service.recommend(
        request.movie_title, 
        request.movie_id, 
        request.media_type
    )
    return RecommendationResponse(
        recommendations=recommendations, 
        source_movie=source_movie
    )
