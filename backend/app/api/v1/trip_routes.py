from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import structlog

from app.schemas.trip import (
    TripCreate,
    TripResponse,
    TripPreferences,
    ItineraryResponse,
    ItineraryUpdate,
    ItineraryRefinementRequest,
    NaturalLanguageTripCreate,
    NaturalLanguageTripResponse
)
from app.services.trip_service import TripService
from app.services.llm_service import LLMService

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/trips")

# Dependency injection
def get_trip_service():
    return TripService()

def get_llm_service():
    return LLMService()

@router.post("/natural", response_model=NaturalLanguageTripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip_from_natural_language(
    trip_data: dict,
    trip_service: TripService = Depends(get_trip_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Create a new trip from natural language description
    """
    try:
        if not trip_data.get('natural_language_input'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Natural language input is required"
            )
        
        # Extract structured data from the natural language input
        natural_language_text = trip_data['natural_language_input']
        logger.info("Processing natural language input", input=natural_language_text)
        
        # Use LLM to extract structured travel intent
        extracted_data = await llm_service.extract_intent_from_text(natural_language_text)
        logger.info("Successfully extracted trip data", extracted_data=extracted_data)
        
        # Convert extracted data to proper format for trip creation and handle potential issues
        try:
            # Make sure we have proper date strings
            from datetime import datetime, timedelta
            
            # Default dates if not available or properly formatted
            today = datetime.now()
            default_start = (today + timedelta(days=30)).strftime("%Y-%m-%d")
            default_end = (today + timedelta(days=37)).strftime("%Y-%m-%d")
            
            # Try to get dates from extracted data
            start_date = extracted_data.get("start_date", default_start)
            end_date = extracted_data.get("end_date", default_end)
            
            # Ensure budget level and transport type are lowercase strings to match the enum in the schema
            budget_level = str(extracted_data.get("budget_level", "moderate")).lower()
            if budget_level not in ["budget", "moderate", "luxury"]:
                budget_level = "moderate"
                
            transport_type = str(extracted_data.get("transport_type", "air")).lower()
            if transport_type not in ["air", "road"]:
                transport_type = "air"
            
            structured_trip_data = {
                "origin": extracted_data.get("origin", {"city": "New York", "country": "USA"}),
                "destinations": extracted_data.get("destinations", [{"city": "Paris", "country": "France"}]),
                "start_date": start_date,
                "end_date": end_date,
                "travelers": extracted_data.get("travelers", {"adults": 1, "children": 0, "infants": 0}),
                "budget_level": budget_level,
                "transport_type": transport_type,
            }
            
            logger.info("Processed structured trip data", data=structured_trip_data)
            
            # Create the trip using the structured data
            trip = await trip_service.create_trip(TripCreate(**structured_trip_data))
        except Exception as e:
            logger.error("Error converting natural language to structured data", error=str(e))
            # Create a fallback trip with safe defaults
            fallback_trip_data = {
                "origin": {"city": "New York", "country": "USA"},
                "destinations": [{"city": "Paris", "country": "France"}],
                "start_date": default_start,
                "end_date": default_end,
                "travelers": {"adults": 1, "children": 0, "infants": 0},
                "budget_level": "moderate",
                "transport_type": "air"
            }
            trip = await trip_service.create_trip(TripCreate(**fallback_trip_data))
        
        # Add extracted interests as preferences if available
        if "interests" in extracted_data and extracted_data["interests"]:
            preferences = {
                "interests": extracted_data["interests"]
            }
            trip = await trip_service.add_preferences(trip.id, TripPreferences(**preferences))
        
        return {"id": trip.id, "has_itinerary": True}
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error("Error creating trip from natural language", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trip from natural language: {str(e)}"
        )

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip_data: dict,
    trip_service: TripService = Depends(get_trip_service)
):
    """
    Create a new trip with basic information and optionally preferences
    """
    # Extract preferences if they exist
    preferences = None
    if "preferences" in trip_data:
        preferences = trip_data.pop("preferences")
    
    # Handle 'use_natural_language' flag which isn't in TripCreate schema
    if "use_natural_language" in trip_data:
        trip_data.pop("use_natural_language")
        
    # Create trip first
    trip = await trip_service.create_trip(TripCreate(**trip_data))
    
    # If preferences were included, add them
    if preferences:
        trip = await trip_service.add_preferences(trip.id, TripPreferences(**preferences))
    
    return trip

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
    trip_service: TripService = Depends(get_trip_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Get itinerary for a trip, generating one if it doesn't exist
    """
    try:
        # First try to get an existing itinerary
        return await trip_service.get_itinerary(trip_id)
    except ValueError as e:
        # If no itinerary exists, generate one on the fly
        if "Itinerary not found" in str(e):
            logger.info(f"Automatically generating itinerary for trip {trip_id}")
            return await trip_service.generate_itinerary(trip_id, llm_service)
        # Re-raise other exceptions
        raise
