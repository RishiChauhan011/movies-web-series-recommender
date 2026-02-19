# FastAPI Setup

This project has been restructured to support FastAPI. The new backend structure is located in `backend/app`.

## Project Structure

- `backend/app/main.py`: The entry point for the FastAPI application.
- `backend/app/api/`: Contains API routes and endpoints.
- `backend/app/core/`: Configuration settings.
- `backend/app/services/`: Business logic (recommendation engine).
- `backend/app/schemas/`: Pydantic models for data validation.
- `backend/model/`: Contains the machine learning models (`.pkl` files).

## Running the API

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```bash
   python -m backend.app.main
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

3. Access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /api/v1/recommender/recommend`: Get movie recommendations.
  - Body: `{"movie_title": "The Dark Knight"}`
