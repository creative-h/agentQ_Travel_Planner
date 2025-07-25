from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.schemas.trip import (
    TripCreate,
    TripResponse,
    TripPreferences,
    ItineraryResponse,
    ItineraryUpdate,
    ItineraryRefinementRequest,
    NaturalLanguageTripCreate
)
from app.services.trip_service import TripService
from app.services.llm_service import LLMService

router = APIRouter(prefix="/trips")

# Dependency injection
def get_trip_service():
    return TripService()

def get_llm_service():
    return LLMService()

@router.post("/natural", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip_from_natural_language(
    trip_data: dict,
    trip_service: TripService = Depends(get_trip_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Create a new trip from natural language description
    """
    try:
        # Just return a successful response for now
        # In production, you would process this with LLM and create a structured trip
        return {"id": 123, "has_itinerary": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trip from natural language: {str(e)}"
        )

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip_data: TripCreate,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Create a new trip with basic information
    """
    return await trip_service.create_trip(trip_data)

@router.post("/{trip_id}/preferences", response_model=TripResponse)
async def add_trip_preferences(
    trip_id: int,
    preferences: TripPreferences,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Add preferences to an existing trip
    """
    return await trip_service.add_preferences(trip_id, preferences)

@router.post("/{trip_id}/generate-itinerary", response_model=ItineraryResponse)
async def generate_itinerary(
    trip_id: int,
    trip_service: TripService = Depends(get_trip_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Generate an AI-powered itinerary based on trip details and preferences
    """
    return await trip_service.generate_itinerary(trip_id, llm_service)

@router.put("/{trip_id}/itinerary", response_model=ItineraryResponse)
async def update_itinerary(
    trip_id: int,
    update_data: ItineraryUpdate,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Update an existing itinerary
    """
    return await trip_service.update_itinerary(trip_id, update_data)

@router.post("/{trip_id}/itinerary/refine", response_model=ItineraryResponse)
async def refine_itinerary(
    trip_id: int,
    refinement: ItineraryRefinementRequest,
    trip_service: TripService = Depends(get_trip_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Refine an itinerary with AI using natural language requests
    """
    return await trip_service.refine_itinerary(trip_id, refinement, llm_service)

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: int,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Get trip details by ID
    """
    return await trip_service.get_trip(trip_id)

@router.get("/{trip_id}/itinerary", response_model=ItineraryResponse)
async def get_itinerary(
    trip_id: int,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Get itinerary for a trip
    """
    return await trip_service.get_itinerary(trip_id)
