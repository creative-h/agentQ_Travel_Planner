import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import LocationAutocomplete from './LocationAutocomplete';
import TravelersCounter from './TravelersCounter';

const TripInitForm = ({ onSubmit }) => {
  // Form state
  const [origin, setOrigin] = useState(null);
  const [destinations, setDestinations] = useState([{ city: '', country: '' }]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [travelers, setTravelers] = useState({ adults: 1, children: 0, infants: 0 });
  const [budgetLevel, setBudgetLevel] = useState('MODERATE');
  const [transportType, setTransportType] = useState('AIR');
  const [naturalLanguageInput, setNaturalLanguageInput] = useState('');
  const [useNaturalLanguage, setUseNaturalLanguage] = useState(true);
  const [errors, setErrors] = useState({});

  // Destination management
  const handleDestinationChange = (index, destination) => {
    const newDestinations = [...destinations];
    newDestinations[index] = destination;
    setDestinations(newDestinations);
  };

  const addDestination = () => {
    setDestinations([...destinations, { city: '', country: '' }]);
  };

  const removeDestination = (index) => {
    if (destinations.length > 1) {
      const newDestinations = destinations.filter((_, i) => i !== index);
      setDestinations(newDestinations);
    }
  };

  // Form validation
  const validateForm = () => {
    const newErrors = {};

    if (useNaturalLanguage) {
      // Validate natural language input
      if (!naturalLanguageInput.trim()) {
        newErrors.naturalLanguageInput = 'Please describe your trip';
      }
    } else {
      // Validate structured form
      if (!origin || !origin.city || !origin.country) {
        newErrors.origin = 'Please select an origin city';
      }

      const hasInvalidDestination = destinations.some(
        dest => !dest || !dest.city || !dest.country
      );
      
      if (hasInvalidDestination) {
        newErrors.destinations = 'Please select all destination cities';
      }

      if (!startDate) {
        newErrors.startDate = 'Please select a start date';
      }

      if (!endDate) {
        newErrors.endDate = 'Please select an end date';
      }

      if (startDate && endDate && startDate > endDate) {
        newErrors.dateRange = 'End date must be after start date';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    if (useNaturalLanguage) {
      // Submit natural language input
      const tripData = {
        natural_language_input: naturalLanguageInput,
        use_natural_language: true,
        // Default values needed by the backend
        origin: null,
        destinations: [],
        start_date: null,
        end_date: null,
        travelers: { adults: 1, children: 0, infants: 0 },
        budget_level: 'MODERATE',
        transport_type: 'AIR'
      };
      onSubmit(tripData);
    } else {
      // Submit structured form data
      const tripData = {
        origin,
        destinations: destinations.filter(dest => dest.city && dest.country),
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        travelers,
        budget_level: budgetLevel,
        transport_type: transportType,
        use_natural_language: false
      };
      onSubmit(tripData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Natural Language Input - Main Option */}
      <div className="trip-form-card">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Describe your trip in your own words</h3>
        <p className="text-gray-600 mb-4">
          Tell us about your ideal trip in natural language, and our AI will create a personalized itinerary for you.
        </p>

        <div>
          <label htmlFor="naturalLanguageInput" className="form-label">Your perfect trip looks like...</label>
          <textarea
            id="naturalLanguageInput"
            rows="5"
            className="form-input w-full"
            placeholder="e.g., I want to spend 5 days in Paris exploring art museums, trying local cuisine, and taking day trips to nearby towns. I prefer boutique hotels and want to avoid tourist traps."
            value={naturalLanguageInput}
            onChange={(e) => setNaturalLanguageInput(e.target.value)}
          ></textarea>
          {errors.naturalLanguageInput && <p className="mt-1 text-sm text-red-600">{errors.naturalLanguageInput}</p>}
        </div>
      </div>

      {/* Toggle between natural language and structured form */}
      <div className="flex justify-center">
        <button 
          type="button" 
          onClick={() => setUseNaturalLanguage(!useNaturalLanguage)}
          className="text-primary-600 hover:text-primary-800 flex items-center"
        >
          <span className="mr-2">{useNaturalLanguage ? 'Or fill out the structured form instead' : 'Back to natural language input'}</span>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M15.707 10.707a1 1 0 01-1.414 0L12 8.414V15a1 1 0 11-2 0V8.414l-2.293 2.293a1 1 0 11-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Structured Form - Alternative Option */}
      {!useNaturalLanguage && (
        <div className="space-y-8">
          {/* Origin & Destinations */}
          <div className="trip-form-card space-y-6">
            <div>
              <label htmlFor="origin" className="form-label">Origin</label>
              <LocationAutocomplete
                id="origin"
                placeholder="Where are you starting from?"
                value={origin}
                onChange={setOrigin}
              />
              {errors.origin && <p className="mt-1 text-sm text-red-600">{errors.origin}</p>}
            </div>

            <div>
              <label className="form-label">Destinations</label>
              {destinations.map((dest, index) => (
                <div key={index} className="flex items-start mb-3">
                  <div className="flex-grow">
                    <LocationAutocomplete
                      id={`destination-${index}`}
                      placeholder="Where are you going?"
                      value={dest}
                      onChange={(location) => handleDestinationChange(index, location)}
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeDestination(index)}
                    className="ml-2 mt-2 text-gray-400 hover:text-gray-600"
                    disabled={destinations.length <= 1}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              ))}
              {errors.destinations && <p className="mt-1 text-sm text-red-600">{errors.destinations}</p>}
              
              <button
                type="button"
                onClick={addDestination}
                className="flex items-center text-primary-600 hover:text-primary-800 mt-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Add another destination
              </button>
            </div>
          </div>

          {/* Travel Dates */}
          <div className="trip-form-card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Travel Dates</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="startDate" className="form-label">Start Date</label>
                <DatePicker
                  id="startDate"
                  selected={startDate}
                  onChange={date => setStartDate(date)}
                  selectsStart
                  startDate={startDate}
                  endDate={endDate}
                  minDate={new Date()}
                  className="form-input"
                  placeholderText="Select start date"
                />
                {errors.startDate && <p className="mt-1 text-sm text-red-600">{errors.startDate}</p>}
              </div>

              <div>
                <label htmlFor="endDate" className="form-label">End Date</label>
                <DatePicker
                  id="endDate"
                  selected={endDate}
                  onChange={date => setEndDate(date)}
                  selectsEnd
                  startDate={startDate}
                  endDate={endDate}
                  minDate={startDate}
                  className="form-input"
                  placeholderText="Select end date"
                />
                {errors.endDate && <p className="mt-1 text-sm text-red-600">{errors.endDate}</p>}
              </div>
            </div>

            {errors.dateRange && <p className="mt-3 text-sm text-red-600">{errors.dateRange}</p>}
          </div>

          {/* Travel Preferences */}
          <div className="trip-form-card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Travel Preferences</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="form-label">Travelers</label>
                <TravelersCounter value={travelers} onChange={setTravelers} />
              </div>

              <div>
                <label htmlFor="budgetLevel" className="form-label">Budget Level</label>
                <select
                  id="budgetLevel"
                  value={budgetLevel}
                  onChange={(e) => setBudgetLevel(e.target.value)}
                  className="form-input"
                >
                  <option value="BUDGET">Budget</option>
                  <option value="MODERATE">Moderate</option>
                  <option value="LUXURY">Luxury</option>
                </select>
              </div>
            </div>

            <div className="mt-6">
              <label className="form-label">Transport Type</label>
              <div className="mt-2 flex space-x-4">
                <label className="inline-flex items-center">
                  <input
                    type="radio"
                    name="transportType"
                    value="AIR"
                    checked={transportType === 'AIR'}
                    onChange={() => setTransportType('AIR')}
                    className="h-4 w-4 text-primary-600 border-gray-300 focus:ring-primary-500"
                  />
                  <span className="ml-2">Air Travel</span>
                </label>
                <label className="inline-flex items-center">
                  <input
                    type="radio"
                    name="transportType"
                    value="ROAD"
                    checked={transportType === 'ROAD'}
                    onChange={() => setTransportType('ROAD')}
                    className="h-4 w-4 text-primary-600 border-gray-300 focus:ring-primary-500"
                  />
                  <span className="ml-2">Road Trip</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-end">
        <button type="submit" className="btn btn-primary">
          {useNaturalLanguage ? 'Create My Trip' : 'Continue to Preferences'}
        </button>
      </div>
    </form>
  );
};

export default TripInitForm;
