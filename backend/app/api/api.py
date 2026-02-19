from fastapi import APIRouter
from backend.app.api.endpoints import recommender, tmdb

api_router = APIRouter()
api_router.include_router(recommender.router, prefix="/recommender", tags=["recommender"])
api_router.include_router(tmdb.router, prefix="/tmdb", tags=["TMDB"])
