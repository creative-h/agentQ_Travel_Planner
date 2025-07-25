import json
from typing import Dict, List, Any, Optional
import structlog
import aiohttp
from datetime import datetime, date, timedelta
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
            - budget_level (string: "budget", "moderate", or "luxury")
            - transport_type (string: "air" or "road")
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
              "budget_level": "moderate",
              "transport_type": "air",
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
                    "budget_level": "moderate",
                    "transport_type": "air",
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
                "budget_level": "moderate",
                "transport_type": "air",
                "interests": ["sightseeing"]
            }

    async def generate_itinerary(self, trip_data: TripResponse) -> Itinerary:
        """
        Generate a detailed day-by-day itinerary based on trip data
        """
        try:
            # Extract relevant trip information for the prompt
            origin = f"{trip_data.origin.city}, {trip_data.origin.country}"
            
            destinations = []
            for destination in trip_data.destinations:
                destinations.append(f"{destination.city}, {destination.country}")
                
            destinations_str = ", ".join(destinations)
            
            # Format dates
            start_date = trip_data.start_date.strftime("%Y-%m-%d") if trip_data.start_date else "TBD"
            end_date = trip_data.end_date.strftime("%Y-%m-%d") if trip_data.end_date else "TBD"
            
            # Calculate duration
            duration = "unknown"
            if trip_data.start_date and trip_data.end_date:
                duration = (trip_data.end_date - trip_data.start_date).days + 1
            
            # Get preferences
            interests = []
            if hasattr(trip_data, "preferences") and trip_data.preferences:
                # Handle both dictionary and object cases
                if isinstance(trip_data.preferences, dict):
                    interests = trip_data.preferences.get("interests", [])
                elif hasattr(trip_data.preferences, "interests"):
                    # Access as an object property
                    interests = trip_data.preferences.interests if trip_data.preferences.interests else []
                
            interests_str = ", ".join(interests) if interests else "general sightseeing"
            
            # Create prompt for LLM
            prompt = f"""
            Generate a detailed travel itinerary for a trip with the following details:
            - Origin: {origin}
            - Destination(s): {destinations_str}
            - Start date: {start_date}
            - End date: {end_date}
            - Duration: {duration} days
            - Budget level: {trip_data.budget_level}
            - Transport type: {trip_data.transport_type}
            - Interests: {interests_str}
            
            Return a JSON object with the structure:
            
            {{
                "days": [
                    {{
                        "day_number": 1,
                        "date": "{start_date if start_date != 'TBD' else '2025-08-01'}",
                        "activities": [
                            {{
                                "name": "Activity name",
                                "description": "Activity description",
                                "location": {{"city": "City name", "country": "Country name"}},
                                "start_time": "09:00",
                                "end_time": "11:00",
                                "cost_estimate": 30.0
                            }}
                        ],
                        "transportation": [
                            {{
                                "type": "Type of transport",
                                "departure_location": {{"city": "City name", "country": "Country name"}},
                                "arrival_location": {{"city": "City name", "country": "Country name"}},
                                "departure_time": "08:00",
                                "arrival_time": "09:00",
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
            
            Make sure each date is in YYYY-MM-DD format. Times should be HH:MM format.
            Return ONLY valid JSON without any explanations or additional text.
            """
            
            response = await self._make_llm_request([{"role": "user", "content": prompt}], temperature=0.7)
            content = response
            logger.info("Raw LLM itinerary response", content=content[:200] + "...")
            
            # Extract JSON from the response
            try:
                # Extract just the JSON part if needed
                try:
                    start_idx = content.find('{')
                    end_idx = content.rfind('}')
                    if start_idx >= 0 and end_idx >= 0:
                        content = content[start_idx:end_idx+1]
                except Exception:
                    pass
                
                parsed_content = json.loads(content)
                
                # Process the days data to ensure it's valid
                processed_days = []
                for day in parsed_content.get("days", []):
                    # Format the date string correctly
                    try:
                        date_str = day.get("date")
                        # Ensure the date is valid or use a default
                        if not date_str or len(date_str) < 8:
                            if trip_data.start_date:
                                day_num = day.get("day_number", 1) - 1
                                day_date = trip_data.start_date + timedelta(days=day_num)
                                day["date"] = day_date.strftime("%Y-%m-%d")
                            else:
                                today = datetime.now().date()
                                day["date"] = today.strftime("%Y-%m-%d")
                    except Exception as e:
                        logger.warning(f"Error processing date for day {day.get('day_number', '?')}: {str(e)}")
                        # Use today's date as fallback
                        day["date"] = datetime.now().date().strftime("%Y-%m-%d")
                    
                    # Process transportation to ensure it has valid times
                    if "transportation" in day:
                        for transport in day["transportation"]:
                            if not transport.get("departure_time") or not isinstance(transport["departure_time"], str):
                                transport["departure_time"] = "08:00"
                            if not transport.get("arrival_time") or not isinstance(transport["arrival_time"], str):
                                transport["arrival_time"] = "09:00"
                    
                    processed_days.append(day)
                
                # Create itinerary object
                itinerary_data = {
                    "trip_id": trip_data.id,
                    "days": processed_days,
                    "total_cost_estimate": parsed_content.get("total_cost_estimate"),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                
                logger.info("Successfully generated itinerary", trip_id=trip_data.id)
                return Itinerary(**itinerary_data)
                
            except json.JSONDecodeError as e:
                logger.error("Failed to parse LLM response as JSON", error=str(e))
                # Create a default itinerary instead of failing
                return self._create_default_itinerary(trip_data)
                
            except Exception as e:
                logger.error("Error in itinerary processing", error=str(e), trip_id=trip_data.id)
                # Create a default itinerary instead of failing
                return self._create_default_itinerary(trip_data)
                
        except Exception as e:
            logger.error("Failed to generate itinerary", error=str(e), trip_id=trip_data.id)
            # Create a default itinerary instead of failing
            return self._create_default_itinerary(trip_data)
    
    def _create_default_itinerary(self, trip_data: TripResponse) -> Itinerary:
        """
        Create a default itinerary when generation fails
        """
        try:
            logger.info("Creating default itinerary", trip_id=trip_data.id)
            
            # Determine dates
            if trip_data.start_date and trip_data.end_date:
                start_date = trip_data.start_date
                end_date = trip_data.end_date
                duration = (end_date - start_date).days + 1
            else:
                start_date = datetime.now().date() + timedelta(days=30)
                duration = 3
                end_date = start_date + timedelta(days=duration-1)
            
            # Get primary destination
            destination = trip_data.destinations[0] if trip_data.destinations else Location(city="Paris", country="France")
            
            # Create days
            days = []
            for day_num in range(1, duration + 1):
                day_date = start_date + timedelta(days=day_num-1)
                
                # Create a simple day itinerary
                days.append({
                    "day_number": day_num,
                    "date": day_date.strftime("%Y-%m-%d"),
                    "activities": [
                        {
                            "name": f"Explore {destination.city}",
                            "description": f"Discover the sights of {destination.city}",
                            "location": {"city": destination.city, "country": destination.country},
                            "start_time": "09:00",
                            "end_time": "17:00",
                            "cost_estimate": 50.0
                        }
                    ],
                    "transportation": [
                        {
                            "type": trip_data.transport_type if hasattr(trip_data, 'transport_type') else "air",
                            "departure_location": {"city": trip_data.origin.city, "country": trip_data.origin.country},
                            "arrival_location": {"city": destination.city, "country": destination.country},
                            "departure_time": "08:00",
                            "arrival_time": "10:00",
                            "cost_estimate": 200.0
                        }
                    ],
                    "accommodation": {
                        "name": f"{destination.city} Hotel",
                        "location": {"city": destination.city, "country": destination.country},
                        "cost_estimate": 100.0
                    },
                    "notes": f"Day {day_num} in {destination.city}"
                })
            
            itinerary_data = {
                "trip_id": trip_data.id,
                "days": days,
                "total_cost_estimate": 500.0 * duration,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "ai_generated": True
            }
            
            return Itinerary(**itinerary_data)
            
        except Exception as e:
            logger.error("Error creating default itinerary", error=str(e))
            # Create a minimal itinerary if all else fails
            return Itinerary(
                trip_id=trip_data.id,
                days=[],
                total_cost_estimate=0.0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                ai_generated=True
            )

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
