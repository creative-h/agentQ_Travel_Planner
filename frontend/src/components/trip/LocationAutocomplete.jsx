import React, { useState, useEffect, useRef } from 'react';

// Mock location data for demo purposes
// In a real application, this would come from an API like Amadeus or Google Places
const MOCK_LOCATIONS = [
  { city: 'Paris', country: 'France' },
  { city: 'London', country: 'United Kingdom' },
  { city: 'New York', country: 'USA' },
  { city: 'Tokyo', country: 'Japan' },
  { city: 'Rome', country: 'Italy' },
  { city: 'Barcelona', country: 'Spain' },
  { city: 'Berlin', country: 'Germany' },
  { city: 'Sydney', country: 'Australia' },
  { city: 'Amsterdam', country: 'Netherlands' },
  { city: 'Dubai', country: 'UAE' },
  { city: 'Singapore', country: 'Singapore' },
  { city: 'Hong Kong', country: 'China' },
  { city: 'Bangkok', country: 'Thailand' },
  { city: 'Istanbul', country: 'Turkey' },
  { city: 'Prague', country: 'Czech Republic' },
];

const LocationAutocomplete = ({ id, placeholder, value, onChange }) => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const wrapperRef = useRef(null);

  useEffect(() => {
    if (value) {
      setQuery(`${value.city}, ${value.country}`);
    } else {
      setQuery('');
    }
  }, [value]);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [wrapperRef]);

  // Search for locations based on query
  useEffect(() => {
    if (query.trim() === '') {
      setSuggestions([]);
      return;
    }

    const queryLower = query.toLowerCase();
    const filteredLocations = MOCK_LOCATIONS
      .filter(location => 
        location.city.toLowerCase().includes(queryLower) || 
        location.country.toLowerCase().includes(queryLower)
      )
      .slice(0, 5); // Limit to 5 results
    
    setSuggestions(filteredLocations);
  }, [query]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    setIsOpen(true);
    onChange(null); // Clear selection when user types
  };

  const handleSelectLocation = (location) => {
    onChange(location);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={wrapperRef}>
      <input
        type="text"
        id={id}
        className="form-input"
        placeholder={placeholder}
        value={query}
        onChange={handleInputChange}
        onFocus={() => query.trim() !== '' && setIsOpen(true)}
        autoComplete="off"
      />

      {isOpen && suggestions.length > 0 && (
        <ul className="absolute z-10 w-full bg-white border border-gray-300 rounded-md shadow-lg mt-1 max-h-60 overflow-auto">
          {suggestions.map((location, index) => (
            <li 
              key={index}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleSelectLocation(location)}
            >
              <div className="font-medium">{location.city}</div>
              <div className="text-sm text-gray-500">{location.country}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default LocationAutocomplete;
