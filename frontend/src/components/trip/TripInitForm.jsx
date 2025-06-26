import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import LocationAutocomplete from './LocationAutocomplete';
import TravelersCounter from './TravelersCounter';

const TripInitForm = ({ onSubmit }) => {
  const [origin, setOrigin] = useState(null);
  const [destinations, setDestinations] = useState([{ city: '', country: '' }]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [travelers, setTravelers] = useState({ adults: 1, children: 0, infants: 0 });
  const [budgetLevel, setBudgetLevel] = useState('MODERATE');
  const [transportType, setTransportType] = useState('AIR');
  const [errors, setErrors] = useState({});

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

  const validateForm = () => {
    const newErrors = {};

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

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const tripData = {
      origin,
      destinations: destinations.filter(dest => dest.city && dest.country),
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      travelers,
      budget_level: budgetLevel,
      transport_type: transportType,
    };

    onSubmit(tripData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
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

      <div className="flex justify-end">
        <button type="submit" className="btn btn-primary">
          Continue to Preferences
        </button>
      </div>
    </form>
  );
};

export default TripInitForm;
