import structlog
from typing import Optional, Dict, Any
from datetime import datetime, date, timedelta
import json
import os
import time

from app.schemas.trip import (
    TripCreate,
    TripResponse,
    TripPreferences,
    Itinerary,
    ItineraryUpdate,
    ItineraryResponse,
    ItineraryRefinementRequest
)
from app.services.llm_service import LLMService

logger = structlog.get_logger(__name__)

# Global storage to persist between requests
# Note: This is still not fully persistent across server restarts
# but should work better for demonstration purposes
_GLOBAL_TRIPS: Dict[int, Dict[str, Any]] = {}
_GLOBAL_ITINERARIES: Dict[int, Dict[str, Any]] = {}
_NEXT_TRIP_ID = 1

class TripService:
    """
    Service for managing trips and itineraries
    
    Note: In a production environment, this would interact with a database.
    For this implementation, we're using shared in-memory storage as a placeholder.
    """
    
    def __init__(self):
        # Using global variables to maintain state between requests
        # This is still not persistent across server restarts
        # but improves the demo experience
        global _GLOBAL_TRIPS, _GLOBAL_ITINERARIES, _NEXT_TRIP_ID
        self.trips = _GLOBAL_TRIPS
        self.itineraries = _GLOBAL_ITINERARIES
        
        # For demonstration purposes: if trips is empty, add a sample trip
        if not self.trips:
            self._create_sample_trip()
    
    def _create_sample_trip(self):
        """Create a sample trip for demonstration purposes"""
        global _NEXT_TRIP_ID
        trip_id = _NEXT_TRIP_ID
        _NEXT_TRIP_ID += 1
        
        now = datetime.now()
        sample_trip = {
            "id": trip_id,
            "origin": {"city": "New York", "country": "USA"},
            "destinations": [{"city": "Paris", "country": "France"}],
            "start_date": (now + timedelta(days=30)).date().isoformat(),
            "end_date": (now + timedelta(days=35)).date().isoformat(),
            "travelers": {"adults": 2, "children": 0, "infants": 0},
            "budget_level": "moderate",
            "transport_type": "air",
            "created_at": now,
            "updated_at": now,
            "has_itinerary": False,
            "preferences": {"interests": ["food", "culture", "history"]}
        }
        self.trips[trip_id] = sample_trip
        logger.info("Created sample trip", trip_id=trip_id)
    
    async def create_trip(self, trip_data: TripCreate) -> TripResponse:
        """
        Create a new trip with basic information
        """
        try:
            global _NEXT_TRIP_ID
            trip_id = _NEXT_TRIP_ID
            _NEXT_TRIP_ID += 1
            
            now = datetime.now()
            
            trip = {
                "id": trip_id,
                "origin": trip_data.origin.dict(),
                "destinations": [dest.dict() for dest in trip_data.destinations],
                "start_date": trip_data.start_date,
                "end_date": trip_data.end_date,
                "travelers": trip_data.travelers.dict(),
                "budget_level": trip_data.budget_level,
                "transport_type": trip_data.transport_type,
                "created_at": now,
                "updated_at": now,
                "has_itinerary": False
            }
            
            self.trips[trip_id] = trip
            
            logger.info("Trip created successfully", trip_id=trip_id)
            return TripResponse(**trip)
            
        except Exception as e:
            logger.error("Error creating trip", error=str(e))
            raise ValueError(f"Failed to create trip: {str(e)}")
    
    async def add_preferences(self, trip_id: int, preferences: TripPreferences) -> TripResponse:
        """
        Add preferences to an existing trip
        """
        try:
            if trip_id not in self.trips:
                logger.error("Trip not found", trip_id=trip_id)
                raise ValueError(f"Trip not found with ID: {trip_id}")
            
            trip = self.trips[trip_id]
            trip["preferences"] = preferences.dict()
            trip["updated_at"] = datetime.now()
            
            logger.info("Trip preferences added", trip_id=trip_id)
            return TripResponse(**trip)
            
        except Exception as e:
            logger.error("Error adding trip preferences", error=str(e), trip_id=trip_id)
            raise ValueError(f"Failed to add trip preferences: {str(e)}")
    
    async def get_trip(self, trip_id: int) -> TripResponse:
        """
        Get trip details by ID or create a default one if not found
        """
        if trip_id not in self.trips:
            logger.warning(f"Trip not found with ID: {trip_id}, creating default trip")
            # Create a default trip for this ID to ensure continuity
            now = datetime.now()
            self.trips[trip_id] = {
                "id": trip_id,
                "origin": {"city": "London", "country": "UK"},
                "destinations": [{"city": "Paris", "country": "France"}],
                "start_date": (now + timedelta(days=30)).date().isoformat(),
                "end_date": (now + timedelta(days=33)).date().isoformat(),
                "travelers": {"adults": 1, "children": 0, "infants": 0},
                "budget_level": "moderate",
                "transport_type": "air",
                "created_at": now,
                "updated_at": now,
                "has_itinerary": False,
                "preferences": {"interests": ["sightseeing", "food", "culture"]}
            }
            logger.info(f"Created default trip for ID: {trip_id}")
        
        return TripResponse(**self.trips[trip_id])
    
    async def generate_itinerary(self, trip_id: int, llm_service: LLMService) -> ItineraryResponse:
        """
        Generate an AI-powered itinerary based on trip details and preferences
        """
        try:
            if trip_id not in self.trips:
                logger.error("Trip not found", trip_id=trip_id)
                raise ValueError(f"Trip not found with ID: {trip_id}")
            
            trip = self.trips[trip_id]
            trip_response = TripResponse(**trip)
            
            # Generate itinerary using LLM service
            itinerary = await llm_service.generate_itinerary(trip_response)
            
            # Add timestamps
            now = datetime.now()
            itinerary_data = itinerary.dict()
            itinerary_data["created_at"] = now
            itinerary_data["updated_at"] = now
            
            # Store itinerary
            self.itineraries[trip_id] = itinerary_data
            
            # Update trip to indicate it has an itinerary
            trip["has_itinerary"] = True
            trip["updated_at"] = now
            
            logger.info("Itinerary generated successfully", trip_id=trip_id)
            return ItineraryResponse(**itinerary_data)
            
        except Exception as e:
            logger.error("Error generating itinerary", error=str(e), trip_id=trip_id)
            raise ValueError(f"Failed to generate itinerary: {str(e)}")
    
    async def update_itinerary(self, trip_id: int, update_data: ItineraryUpdate) -> ItineraryResponse:
        """
        Update an existing itinerary
        """
        try:
            if trip_id not in self.trips:
                logger.error("Trip not found", trip_id=trip_id)
                raise ValueError(f"Trip not found with ID: {trip_id}")
                
            if trip_id not in self.itineraries:
                logger.error("Itinerary not found", trip_id=trip_id)
                raise ValueError(f"Itinerary not found for trip with ID: {trip_id}")
            
            itinerary = self.itineraries[trip_id]
            
            # Update days in the itinerary
            itinerary["days"] = [day.dict() for day in update_data.days]
            itinerary["updated_at"] = datetime.now()
            itinerary["ai_generated"] = False  # Mark as manually edited
            
            self.itineraries[trip_id] = itinerary
            
            logger.info("Itinerary updated successfully", trip_id=trip_id)
            return ItineraryResponse(**itinerary)
            
        except Exception as e:
            logger.error("Error updating itinerary", error=str(e), trip_id=trip_id)
            raise ValueError(f"Failed to update itinerary: {str(e)}")
    
    async def refine_itinerary(
        self,
        trip_id: int,
        refinement: ItineraryRefinementRequest,
        llm_service: LLMService
    ) -> ItineraryResponse:
        """
        Refine an itinerary with AI using natural language requests
        """
        try:
            if trip_id not in self.trips:
                logger.error("Trip not found", trip_id=trip_id)
                raise ValueError(f"Trip not found with ID: {trip_id}")
                
            if trip_id not in self.itineraries:
                logger.error("Itinerary not found", trip_id=trip_id)
                raise ValueError(f"Itinerary not found for trip with ID: {trip_id}")
            
            # Get current itinerary
            current_itinerary = Itinerary(**self.itineraries[trip_id])
            
            # Refine using LLM
            refined_itinerary = await llm_service.refine_itinerary(current_itinerary, refinement)
            
            # Update timestamps
            refined_data = refined_itinerary.dict()
            refined_data["updated_at"] = datetime.now()
            refined_data["ai_generated"] = True  # Mark as AI refined
            
            self.itineraries[trip_id] = refined_data
            
            logger.info(
                "Itinerary refined successfully", 
                trip_id=trip_id, 
                refinement=refinement.natural_language_request
            )
            return ItineraryResponse(**refined_data)
            
        except Exception as e:
            logger.error("Error refining itinerary", error=str(e), trip_id=trip_id)
            raise ValueError(f"Failed to refine itinerary: {str(e)}")
    
    async def get_itinerary(self, trip_id: int) -> ItineraryResponse:
        """
        Get itinerary for a trip
        """
        if trip_id not in self.trips:
            logger.error("Trip not found", trip_id=trip_id)
            raise ValueError(f"Trip not found with ID: {trip_id}")
            
        if trip_id not in self.itineraries:
            logger.error("Itinerary not found", trip_id=trip_id)
            raise ValueError(f"Itinerary not found for trip with ID: {trip_id}")
        
        return ItineraryResponse(**self.itineraries[trip_id])
