from fastapi import FastAPI
from backend.app.api.api import api_router
from backend.app.core.config import settings
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Recommender API", "docs_url": "/docs"}

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
