import axios from 'axios';

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service methods
const apiService = {
  // Trip endpoints
  createTrip: (tripData) => {
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
