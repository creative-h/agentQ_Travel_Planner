import React from 'react';

const TravelersCounter = ({ value, onChange }) => {
  const { adults, children, infants } = value;

  const handleIncrement = (type) => {
    let newValue = { ...value };
    
    switch (type) {
      case 'adults':
        newValue.adults = Math.min(newValue.adults + 1, 10); // Max 10 adults
        break;
      case 'children':
        newValue.children = Math.min(newValue.children + 1, 10); // Max 10 children
        break;
      case 'infants':
        // Max infants is equal to number of adults
        newValue.infants = Math.min(newValue.infants + 1, newValue.adults);
        break;
      default:
        break;
    }

    onChange(newValue);
  };

  const handleDecrement = (type) => {
    let newValue = { ...value };
    
    switch (type) {
      case 'adults':
        // Minimum 1 adult, and cannot go below number of infants
        newValue.adults = Math.max(newValue.adults - 1, Math.max(1, newValue.infants));
        break;
      case 'children':
        newValue.children = Math.max(newValue.children - 1, 0);
        break;
      case 'infants':
        newValue.infants = Math.max(newValue.infants - 1, 0);
        break;
      default:
        break;
    }

    onChange(newValue);
  };

  const counterSection = (type, label, value, min, max) => {
    const isMinValue = type === 'adults' ? value <= Math.max(1, infants) : value <= min;
    const isMaxValue = type === 'infants' ? value >= adults : value >= max;

    return (
      <div className="flex justify-between items-center py-3 border-b border-gray-200 last:border-b-0">
        <div>
          <p className="font-medium">{label}</p>
          {type === 'infants' && (
            <p className="text-xs text-gray-500">Under 2 years</p>
          )}
          {type === 'children' && (
            <p className="text-xs text-gray-500">2-17 years</p>
          )}
        </div>
        <div className="flex items-center">
          <button
            type="button"
            onClick={() => handleDecrement(type)}
            disabled={isMinValue}
            className={`w-8 h-8 flex items-center justify-center rounded-full border ${
              isMinValue 
                ? 'border-gray-200 text-gray-300 cursor-not-allowed' 
                : 'border-gray-300 text-gray-600 hover:bg-gray-100'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clipRule="evenodd" />
            </svg>
          </button>
          <span className="mx-3 w-6 text-center">{value}</span>
          <button
            type="button"
            onClick={() => handleIncrement(type)}
            disabled={isMaxValue}
            className={`w-8 h-8 flex items-center justify-center rounded-full border ${
              isMaxValue 
                ? 'border-gray-200 text-gray-300 cursor-not-allowed' 
                : 'border-gray-300 text-gray-600 hover:bg-gray-100'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="border border-gray-300 rounded-md overflow-hidden bg-white">
      {counterSection('adults', 'Adults', adults, 1, 10)}
      {counterSection('children', 'Children', children, 0, 10)}
      {counterSection('infants', 'Infants', infants, 0, adults)}
    </div>
  );
};

export default TravelersCounter;
