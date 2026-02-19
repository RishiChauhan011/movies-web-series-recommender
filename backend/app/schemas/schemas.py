from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    movie_title: str
    movie_id: Optional[int] = None
    media_type: Optional[str] = "movie"


class MovieSchema(BaseModel):
    id: int
    title: str
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    overview: Optional[str] = None
    rating: float
    release_date: Optional[str] = None
    genres: Optional[List[str]] = []
    vote_count: int = 0
    runtime: Optional[int] = None
    director: Optional[str] = None
    cast: Optional[List[str]] = []
    keywords: Optional[List[str]] = []
    reasoning: Optional[str] = None
    imdb_id: Optional[str] = None
    media_type: Optional[str] = "movie"
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None

class RecommendationResponse(BaseModel):
    recommendations: List[MovieSchema]
    source_movie: Optional[MovieSchema] = None

class MovieListResponse(BaseModel):
    results: List[MovieSchema]
