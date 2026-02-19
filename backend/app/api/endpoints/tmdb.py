from fastapi import APIRouter
from typing import List
from backend.app.schemas.schemas import MovieSchema
from backend.app.services.tmdb_service import tmdb_service

router = APIRouter()

@router.get("/trending", response_model=List[MovieSchema])
def get_trending():
    return tmdb_service.get_trending()

@router.get("/now-playing", response_model=List[MovieSchema])
def get_now_playing():
    return tmdb_service.get_now_playing()

@router.get("/popular-tv", response_model=List[MovieSchema])
def get_popular_tv():
    return tmdb_service.get_popular_tv()

@router.get("/top-rated", response_model=List[MovieSchema])
def get_top_rated():
    return tmdb_service.get_top_rated()

@router.get("/upcoming", response_model=List[MovieSchema])
def get_upcoming():
    return tmdb_service.get_upcoming()
