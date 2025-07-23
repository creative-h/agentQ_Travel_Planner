import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TripInitForm from '../components/trip/TripInitForm';
import TripPreferencesForm from '../components/trip/TripPreferencesForm';
import apiService from '../services/apiService';

const NewTripPage = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [tripData, setTripData] = useState(null);

  const handleTripInitSubmit = async (data) => {
    // If using natural language input, create the trip immediately
    if (data.use_natural_language) {
      try {
        console.log('Creating trip with natural language input:', data.natural_language_input);
        
        // Make actual API call to create trip
        const response = await apiService.createTrip(data);
        const tripId = response.data.id;
        
        // Navigate directly to the itinerary page
        navigate(`/trips/${tripId}/itinerary`);
      } catch (error) {
        console.error('Error creating trip:', error);
        alert('Failed to create trip. Please try again.');
      }
    } else {
      // Otherwise, proceed to preferences step
      setTripData(data);
      setCurrentStep(2);
      window.scrollTo(0, 0);
    }
  };

  const handlePreferencesSubmit = async (preferences) => {
    try {
      console.log('Creating trip with:', { ...tripData, preferences });
      
      // Make actual API call to create trip with preferences
      const tripData_with_preferences = {
        ...tripData,
        preferences
      };
      const response = await apiService.createTrip(tripData_with_preferences);
      const tripId = response.data.id;

      // Navigate to the itinerary page
      navigate(`/trips/${tripId}/itinerary`);
    } catch (error) {
      console.error('Error creating trip:', error);
      alert('Failed to create trip. Please try again.');
    }
  };

  const handleBack = () => {
    setCurrentStep(1);
    window.scrollTo(0, 0);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Plan Your Next Adventure</h1>
        <p className="text-gray-600">
          Tell us about your trip and let our AI create a personalized itinerary just for you.
        </p>
      </div>

      {/* Progress steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentStep >= 1 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
              1
            </div>
            <div className="ml-4">
              <p className="font-medium">Trip Details</p>
              <p className="text-sm text-gray-500">Basic information</p>
            </div>
          </div>

          <div className="hidden sm:block w-24 h-1 bg-gray-200">
            <div className={`h-full ${currentStep >= 2 ? 'bg-primary-600' : 'bg-gray-200'}`} style={{ width: currentStep >= 2 ? '100%' : '0%' }}></div>
          </div>

          <div className="flex items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentStep >= 2 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
              2
            </div>
            <div className="ml-4">
              <p className="font-medium">Preferences</p>
              <p className="text-sm text-gray-500">What you like</p>
            </div>
          </div>

          <div className="hidden sm:block w-24 h-1 bg-gray-200">
            <div className={`h-full ${currentStep >= 3 ? 'bg-primary-600' : 'bg-gray-200'}`} style={{ width: currentStep >= 3 ? '100%' : '0%' }}></div>
          </div>

          <div className="flex items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full ${currentStep >= 3 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
              3
            </div>
            <div className="ml-4">
              <p className="font-medium">Itinerary</p>
              <p className="text-sm text-gray-500">Your plan</p>
            </div>
          </div>
        </div>
      </div>

      {currentStep === 1 && <TripInitForm onSubmit={handleTripInitSubmit} />}
      {currentStep === 2 && <TripPreferencesForm onSubmit={handlePreferencesSubmit} onBack={handleBack} />}
    </div>
  );
};

export default NewTripPage;
