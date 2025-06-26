from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON, Enum, Boolean, Float
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.schemas.trip import BudgetLevel, TransportType

class Trip(BaseModel):
    """Trip model for storing trip details"""
    __tablename__ = "trips"
    
    origin = Column(JSON, nullable=False)  # JSON for location object
    destinations = Column(JSON, nullable=False)  # JSON array of location objects
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    travelers = Column(JSON, nullable=False)  # JSON for travelers info
    budget_level = Column(Enum(BudgetLevel), nullable=False)
    transport_type = Column(Enum(TransportType), nullable=False)
    preferences = Column(JSON, nullable=True)  # JSON for trip preferences
    
    # Relationships
    itineraries = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan")
    
class Itinerary(BaseModel):
    """Itinerary model for storing itinerary details"""
    __tablename__ = "itineraries"
    
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    days = Column(JSON, nullable=False)  # JSON array of daily itinerary objects
    ai_generated = Column(Boolean, default=True)
    total_cost_estimate = Column(Float, nullable=True)
    
    # Relationships
    trip = relationship("Trip", back_populates="itineraries")
