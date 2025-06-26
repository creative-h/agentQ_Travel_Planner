from fastapi import APIRouter
from app.api.v1 import trip_routes

api_router = APIRouter()

# Include all v1 API routes
api_router.include_router(trip_routes.router, prefix="/v1", tags=["trips"])
