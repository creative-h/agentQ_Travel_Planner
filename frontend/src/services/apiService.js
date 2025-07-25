import axios from 'axios';

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: 'https://agentq-travel-planner-5.onrender.com/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service methods
const apiService = {
  // Trip endpoints
  createTrip: (tripData) => {
    // Check if this is a natural language input
    if (tripData.use_natural_language) {
      return api.post('/trips/natural', tripData);
    }
    // Regular structured trip creation
    return api.post('/trips/', tripData);
  },
  
  addTripPreferences: (tripId, preferences) => {
    return api.post(`/trips/${tripId}/preferences`, preferences);
  },
  
  getTrip: (tripId) => {
    return api.get(`/trips/${tripId}`);
  },
  
  // Itinerary endpoints
  generateItinerary: (tripId) => {
    return api.post(`/trips/${tripId}/generate-itinerary`);
  },
  
  getItinerary: (tripId) => {
    return api.get(`/trips/${tripId}/itinerary`);
  },
  
  updateItinerary: (tripId, itineraryData) => {
    return api.put(`/trips/${tripId}/itinerary`, itineraryData);
  },
  
  refineItinerary: (tripId, refinementRequest) => {
    return api.post(`/trips/${tripId}/itinerary/refine`, refinementRequest);
  },
};

export default apiService;
