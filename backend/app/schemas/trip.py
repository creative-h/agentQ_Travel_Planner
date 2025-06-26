from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import date, datetime


class TransportType(str, Enum):
    AIR = "air"
    ROAD = "road"


class BudgetLevel(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class TravelersInfo(BaseModel):
    adults: int = Field(1, ge=1, description="Number of adults (18+ years)")
    children: int = Field(0, ge=0, description="Number of children (2-17 years)")
    infants: int = Field(0, ge=0, description="Number of infants (under 2 years)")


class Location(BaseModel):
    city: str
    country: str
    coordinates: Optional[Dict[str, float]] = None


class TripCreate(BaseModel):
    origin: Location
    destinations: List[Location]
    start_date: date
    end_date: date
    travelers: TravelersInfo
    budget_level: BudgetLevel
    transport_type: TransportType

    @validator("end_date")
    def end_date_must_be_after_start_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be after start date")
        return v


class TripPreferences(BaseModel):
    interests: List[str] = Field(
        ..., description="List of interests/vibes for the trip destinations"
    )
    accommodations: Optional[List[str]] = None
    dining_preferences: Optional[List[str]] = None
    activities_preferences: Optional[List[str]] = None
    special_requirements: Optional[str] = None


class Activity(BaseModel):
    name: str
    description: str
    location: Optional[Location] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    cost_estimate: Optional[float] = None
    booking_url: Optional[str] = None
    notes: Optional[str] = None


class Accommodation(BaseModel):
    name: str
    location: Location
    check_in_date: date
    check_out_date: date
    booking_url: Optional[str] = None
    cost_estimate: Optional[float] = None
    notes: Optional[str] = None


class Transportation(BaseModel):
    type: str
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    departure_location: Optional[Location] = None
    arrival_location: Optional[Location] = None
    booking_reference: Optional[str] = None
    booking_url: Optional[str] = None
    cost_estimate: Optional[float] = None
    notes: Optional[str] = None


class DailyItinerary(BaseModel):
    day_number: int
    date: date
    activities: List[Activity]
    meals: Optional[List[Activity]] = None
    transportation: Optional[List[Transportation]] = None
    accommodation: Optional[Accommodation] = None
    notes: Optional[str] = None


class Itinerary(BaseModel):
    trip_id: int
    days: List[DailyItinerary]
    ai_generated: bool = True
    total_cost_estimate: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ItineraryUpdate(BaseModel):
    days: List[DailyItinerary]


class ItineraryRefinementRequest(BaseModel):
    natural_language_request: str = Field(
        ..., 
        description="User's request to refine the itinerary (e.g., 'Add more outdoor activities on day 3')"
    )
    specific_day: Optional[int] = Field(
        None, 
        description="Optional specific day number to refine (1-indexed)"
    )


class Trip(BaseModel):
    id: int
    origin: Location
    destinations: List[Location]
    start_date: date
    end_date: date
    travelers: TravelersInfo
    budget_level: BudgetLevel
    transport_type: TransportType
    preferences: Optional[TripPreferences] = None
    created_at: datetime
    updated_at: datetime


class TripResponse(Trip):
    has_itinerary: bool = False


class ItineraryResponse(Itinerary):
    pass
