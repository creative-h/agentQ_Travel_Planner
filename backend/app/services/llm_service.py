import json
from typing import Dict, List, Any, Optional
import structlog
from groq import Groq
from pydantic import ValidationError

from app.config.settings import settings
from app.schemas.trip import TripResponse, Itinerary, ItineraryRefinementRequest

logger = structlog.get_logger(__name__)

class LLMService:
    """
    Service for interacting with LLM APIs (e.g., Groq's LLaMa 3)
    """
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set, LLM service will not function properly")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL
        
    async def extract_intent_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract structured travel intent from free-text input
        """
        try:
            prompt = f"""
            Extract structured travel intent from the following text. Return a JSON object with:
            - origin (city, country)
            - destinations (list of city, country)
            - date range (start_date, end_date in YYYY-MM-DD format)
            - travelers (adults, children, infants)
            - budget_level (budget, moderate, luxury)
            - transport_type (air, road)
            - interests (list of strings)

            Text: {text}

            Return ONLY valid JSON without any explanations or additional text.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000,
            )
            
            content = response.choices[0].message.content
            parsed_content = json.loads(content)
            logger.info("Successfully extracted intent from text", input=text)
            return parsed_content
            
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error("Failed to extract intent from text", error=str(e), input=text)
            return {"error": "Failed to extract intent from text"}
    
    async def generate_itinerary(self, trip_data: TripResponse) -> Itinerary:
        """
        Generate a detailed day-by-day itinerary based on trip data
        """
        try:
            # Format the trip data for the prompt
            destinations_str = ", ".join([f"{d.city}, {d.country}" for d in trip_data.destinations])
            interests_str = ", ".join(trip_data.preferences.interests) if trip_data.preferences and trip_data.preferences.interests else "general tourism"
            duration_days = (trip_data.end_date - trip_data.start_date).days + 1
            
            prompt = f"""
            Create a detailed {duration_days}-day travel itinerary for a trip to {destinations_str} for {trip_data.travelers.adults} adults, {trip_data.travelers.children} children, and {trip_data.travelers.infants} infants.
            
            Trip details:
            - Budget level: {trip_data.budget_level.value}
            - Transport type: {trip_data.transport_type.value}
            - Travel dates: {trip_data.start_date} to {trip_data.end_date}
            - Interests: {interests_str}
            
            For each day, please provide:
            1. 3-5 activities with descriptions, estimated times, and approximate costs
            2. Meal suggestions (breakfast, lunch, dinner)
            3. Transportation details between locations
            4. Accommodation recommendations
            
            Return the response as detailed JSON with the following structure:
            {{
                "days": [
                    {{
                        "day_number": 1,
                        "date": "YYYY-MM-DD",
                        "activities": [
                            {{
                                "name": "Activity name",
                                "description": "Detailed description",
                                "location": {{"city": "City name", "country": "Country name"}},
                                "start_time": "HH:MM",
                                "end_time": "HH:MM",
                                "cost_estimate": 50.0,
                                "notes": "Any additional notes"
                            }}
                        ],
                        "meals": [
                            {{
                                "name": "Restaurant name for breakfast/lunch/dinner",
                                "description": "Type of cuisine and recommendations",
                                "location": {{"city": "City name", "country": "Country name"}},
                                "cost_estimate": 30.0
                            }}
                        ],
                        "transportation": [
                            {{
                                "type": "Type of transport",
                                "departure_location": {{"city": "City name", "country": "Country name"}},
                                "arrival_location": {{"city": "City name", "country": "Country name"}},
                                "departure_time": "HH:MM",
                                "arrival_time": "HH:MM",
                                "cost_estimate": 20.0
                            }}
                        ],
                        "accommodation": {{
                            "name": "Hotel/accommodation name",
                            "location": {{"city": "City name", "country": "Country name"}},
                            "cost_estimate": 150.0
                        }},
                        "notes": "Overall day notes"
                    }}
                ],
                "total_cost_estimate": 2500.0
            }}
            
            Return ONLY valid JSON without any explanations or additional text.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000,
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from the response
            try:
                parsed_content = json.loads(content)
                
                # Create itinerary object
                itinerary_data = {
                    "trip_id": trip_data.id,
                    "days": parsed_content.get("days", []),
                    "total_cost_estimate": parsed_content.get("total_cost_estimate"),
                }
                
                logger.info("Successfully generated itinerary", trip_id=trip_data.id)
                return Itinerary(**itinerary_data)
                
            except json.JSONDecodeError as e:
                logger.error("Failed to parse LLM response as JSON", error=str(e))
                raise ValueError("Failed to generate itinerary: Invalid LLM response format")
                
        except Exception as e:
            logger.error("Failed to generate itinerary", error=str(e), trip_id=trip_data.id)
            raise ValueError(f"Failed to generate itinerary: {str(e)}")
    
    async def refine_itinerary(self, 
                              itinerary: Itinerary, 
                              refinement: ItineraryRefinementRequest) -> Itinerary:
        """
        Refine an existing itinerary based on natural language feedback
        """
        try:
            # Prepare the current itinerary as context
            itinerary_json = itinerary.model_dump_json()
            
            specific_day = ""
            if refinement.specific_day is not None:
                specific_day = f"for day {refinement.specific_day}"
            
            prompt = f"""
            I have an existing travel itinerary and I need to refine it {specific_day} based on the following request:
            
            "{refinement.natural_language_request}"
            
            Current itinerary:
            {itinerary_json}
            
            Please modify the itinerary according to the request and return the complete updated itinerary as JSON.
            Keep the same structure but update the relevant parts only.
            Return ONLY valid JSON without any explanations or additional text.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000,
            )
            
            content = response.choices[0].message.content
            
            try:
                parsed_content = json.loads(content)
                
                # Ensure the refined itinerary has the same trip_id
                if "trip_id" not in parsed_content:
                    parsed_content["trip_id"] = itinerary.trip_id
                    
                refined_itinerary = Itinerary(**parsed_content)
                logger.info("Successfully refined itinerary", 
                           trip_id=itinerary.trip_id, 
                           refinement=refinement.natural_language_request)
                return refined_itinerary
                
            except (json.JSONDecodeError, ValidationError) as e:
                logger.error("Failed to parse refined itinerary", error=str(e))
                raise ValueError("Failed to refine itinerary: Invalid response format")
                
        except Exception as e:
            logger.error("Failed to refine itinerary", 
                       error=str(e), 
                       trip_id=itinerary.trip_id)
            raise ValueError(f"Failed to refine itinerary: {str(e)}")
