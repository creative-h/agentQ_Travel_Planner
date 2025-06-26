import React, { useState } from 'react';

const INTEREST_OPTIONS = [
  { id: 'art', label: 'Art & Museums' },
  { id: 'history', label: 'History & Culture' },
  { id: 'food', label: 'Food & Dining' },
  { id: 'nature', label: 'Nature & Outdoors' },
  { id: 'adventure', label: 'Adventure & Sports' },
  { id: 'relaxation', label: 'Relaxation & Wellness' },
  { id: 'nightlife', label: 'Nightlife & Entertainment' },
  { id: 'shopping', label: 'Shopping' },
  { id: 'family', label: 'Family-Friendly Activities' },
  { id: 'local', label: 'Local Experiences' },
  { id: 'photography', label: 'Photography Spots' },
  { id: 'architecture', label: 'Architecture' },
];

const TripPreferencesForm = ({ onSubmit, onBack }) => {
  const [interests, setInterests] = useState([]);
  const [accommodationPrefs, setAccommodationPrefs] = useState('');
  const [diningPrefs, setDiningPrefs] = useState('');
  const [activityPrefs, setActivityPrefs] = useState('');
  const [specialRequirements, setSpecialRequirements] = useState('');
  const [errors, setErrors] = useState({});

  const handleInterestToggle = (interest) => {
    if (interests.includes(interest)) {
      setInterests(interests.filter(i => i !== interest));
    } else {
      setInterests([...interests, interest]);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (interests.length === 0) {
      newErrors.interests = 'Please select at least one interest';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const preferences = {
      interests,
      accommodations: accommodationPrefs ? accommodationPrefs.split(',').map(item => item.trim()) : [],
      dining_preferences: diningPrefs ? diningPrefs.split(',').map(item => item.trim()) : [],
      activities_preferences: activityPrefs ? activityPrefs.split(',').map(item => item.trim()) : [],
      special_requirements: specialRequirements || null,
    };

    onSubmit(preferences);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Interests */}
      <div className="trip-form-card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">What are you interested in experiencing?</h3>
        <p className="text-gray-600 mb-4">Select all that apply. This helps our AI build a personalized itinerary.</p>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {INTEREST_OPTIONS.map((option) => (
            <div key={option.id} className="col-span-1">
              <button
                type="button"
                onClick={() => handleInterestToggle(option.id)}
                className={`w-full py-3 px-4 text-left border rounded-lg focus:outline-none ${
                  interests.includes(option.id)
                    ? 'bg-primary-50 border-primary-300 text-primary-700 ring-2 ring-primary-200'
                    : 'border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>{option.label}</span>
                  {interests.includes(option.id) && (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
              </button>
            </div>
          ))}
        </div>
        {errors.interests && <p className="mt-2 text-sm text-red-600">{errors.interests}</p>}
      </div>

      {/* Additional Preferences */}
      <div className="trip-form-card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Preferences (Optional)</h3>

        <div className="space-y-6">
          <div>
            <label htmlFor="accommodationPrefs" className="form-label">Accommodation Preferences</label>
            <input
              type="text"
              id="accommodationPrefs"
              className="form-input"
              value={accommodationPrefs}
              onChange={(e) => setAccommodationPrefs(e.target.value)}
              placeholder="e.g., Boutique hotels, close to city center, quiet"
            />
            <p className="text-xs text-gray-500 mt-1">Separate preferences with commas</p>
          </div>

          <div>
            <label htmlFor="diningPrefs" className="form-label">Dining Preferences</label>
            <input
              type="text"
              id="diningPrefs"
              className="form-input"
              value={diningPrefs}
              onChange={(e) => setDiningPrefs(e.target.value)}
              placeholder="e.g., Local cuisine, vegetarian options, fine dining"
            />
            <p className="text-xs text-gray-500 mt-1">Separate preferences with commas</p>
          </div>

          <div>
            <label htmlFor="activityPrefs" className="form-label">Activity Preferences</label>
            <input
              type="text"
              id="activityPrefs"
              className="form-input"
              value={activityPrefs}
              onChange={(e) => setActivityPrefs(e.target.value)}
              placeholder="e.g., Walking tours, museums, outdoor activities"
            />
            <p className="text-xs text-gray-500 mt-1">Separate preferences with commas</p>
          </div>
        </div>
      </div>

      {/* Special Requirements */}
      <div className="trip-form-card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Special Requirements</h3>

        <div>
          <label htmlFor="specialRequirements" className="form-label">Anything else we should know?</label>
          <textarea
            id="specialRequirements"
            rows="4"
            className="form-input"
            value={specialRequirements}
            onChange={(e) => setSpecialRequirements(e.target.value)}
            placeholder="e.g., Accessibility needs, dietary restrictions, traveling with pets"
          ></textarea>
        </div>
      </div>

      {/* Free Text Input for AI */}
      <div className="trip-form-card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Or tell us in your own words</h3>
        <p className="text-gray-600 mb-4">
          Alternatively, describe your ideal trip in natural language, and our AI will extract your preferences.
        </p>

        <div>
          <label htmlFor="freeText" className="form-label">Your perfect trip looks like...</label>
          <textarea
            id="freeText"
            rows="4"
            className="form-input"
            placeholder="e.g., I want to spend 5 days in Paris exploring art museums, trying local cuisine, and taking day trips to nearby towns. I prefer boutique hotels and want to avoid tourist traps."
          ></textarea>
        </div>
      </div>

      <div className="flex justify-between">
        <button 
          type="button" 
          onClick={onBack}
          className="btn btn-secondary"
        >
          Back
        </button>
        <button type="submit" className="btn btn-primary">
          Generate Itinerary
        </button>
      </div>
    </form>
  );
};

export default TripPreferencesForm;
