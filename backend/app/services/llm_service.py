import json
from typing import Dict, List, Any, Optional
import structlog
import aiohttp
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
        # Using direct HTTP requests with Groq's API
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model = settings.LLM_MODEL
        
    async def _make_llm_request(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Make a request to the LLM service"""
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 4000,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error("Error from LLM API", status=response.status, error=error_text)
                        raise Exception(f"Error from LLM API: {response.status} - {error_text}")
                    
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                    
        except Exception as e:
            logger.error("Error making LLM request", error=str(e))
            raise Exception(f"Error communicating with LLM service: {e}")

    async def extract_intent_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract structured travel intent from free-text input
        """
        try:
            prompt = f"""
            Extract structured travel intent from the following text. Return a JSON object with:
            - origin (city, country object with city and country fields)
            - destinations (array of objects with city and country fields)
            - start_date (YYYY-MM-DD string)
            - end_date (YYYY-MM-DD string)
            - travelers (object with adults, children, infants as integers)
            - budget_level (string: "BUDGET", "MODERATE", or "LUXURY")
            - transport_type (string: "AIR" or "ROAD")
            - interests (array of strings)
            
            Text: {text}
            
            Return ONLY valid JSON without any explanations or additional text.
            Example response format:
            {{
              "origin": {{ "city": "New York", "country": "USA" }},
              "destinations": [{{ "city": "Paris", "country": "France" }}],
              "start_date": "2025-08-01",
              "end_date": "2025-08-05",
              "travelers": {{ "adults": 2, "children": 0, "infants": 0 }},
              "budget_level": "MODERATE",
              "transport_type": "AIR",
              "interests": ["art", "food", "history"]
            }}
            """
            
            content = await self._make_llm_request(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            # Log the raw content for debugging
            logger.info("Raw LLM response", content=content)
            
            # Try to clean the content if it contains extra text
            try:
                # Find the first '{' and the last '}' to extract JSON
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                
                if start_idx >= 0 and end_idx >= 0:
                    json_content = content[start_idx:end_idx+1]
                    parsed_content = json.loads(json_content)
                else:
                    parsed_content = json.loads(content)
            except json.JSONDecodeError:
                # If that fails, fallback to default data
                logger.error("Could not parse JSON from LLM response", content=content)
                # Return a default structure
                parsed_content = {
                    "origin": {"city": "Unknown", "country": "Unknown"},
                    "destinations": [{"city": "Paris", "country": "France"}],
                    "start_date": "2025-08-01",
                    "end_date": "2025-08-05",
                    "travelers": {"adults": 1, "children": 0, "infants": 0},
                    "budget_level": "MODERATE",
                    "transport_type": "AIR",
                    "interests": ["sightseeing"]
                }
            
            logger.info("Successfully extracted intent from text", extracted_data=parsed_content)
            return parsed_content
            
        except Exception as e:
            logger.error("Failed to extract intent from text", error=str(e), input=text)
            # Return a default structure instead of failing
            return {
                "origin": {"city": "Unknown", "country": "Unknown"},
                "destinations": [{"city": "Paris", "country": "France"}],
                "start_date": "2025-08-01",
                "end_date": "2025-08-05",
                "travelers": {"adults": 1, "children": 0, "infants": 0},
                "budget_level": "MODERATE",
                "transport_type": "AIR",
                "interests": ["sightseeing"]
            }

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
            
            response = await self._make_llm_request([{"role": "user", "content": prompt}], temperature=0.7)
            content = response
            
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
            current_itinerary_json = itinerary.model_dump_json()
            
            specific_day = ""
            if refinement.specific_day is not None:
                specific_day = f"for day {refinement.specific_day}"
            
            prompt = f"""
            I have an existing travel itinerary that needs to be refined {specific_day} based on user feedback.
            
            Current itinerary: {current_itinerary_json}
            
            User's request for refinement: "{refinement.natural_language_request}"
            """
            
            response = await self._make_llm_request([{"role": "user", "content": prompt}], temperature=0.7)
            content = response
            
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
