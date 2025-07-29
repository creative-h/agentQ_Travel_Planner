import React from 'react';
import { 
  PlaneIcon, BedIcon, StarIcon, CheckCircleIcon, CalendarDaysIcon, 
  ClockIcon, BanknotesIcon, BuildingStorefrontIcon, LinkIcon, 
  InformationCircleIcon, PrayerIcon, MountainIcon, SpaIcon
} from '../icons';

// Star Rating component
const StarRatingDisplay = ({ rating }) => {
  return (
    <div className="flex items-center">
      {Array(5).fill(0).map((_, i) => (
        <StarIcon key={i} className={`h-5 w-5 ${i < Math.round(rating) ? 'text-yellow-400' : 'text-gray-300'}`} />
      ))}
      <span className="ml-1 text-sm text-gray-600">({rating ? rating.toFixed(1) : 'N/A'})</span>
    </div>
  );
};

// Package Type Icon component
const PackageTypeIcon = ({ type, className }) => {
  switch (type.toLowerCase()) {
    case 'religious':
      return <PrayerIcon className={className} />;
    case 'thrill':
      return <MountainIcon className={className} />;
    case 'relaxing':
      return <SpaIcon className={className} />;
    default:
      return <InformationCircleIcon className={className} />;
  }
};

const PackageCard = ({ travelPackage, onSelect, isSelected = false }) => {
  const { flight, hotel, type, sources } = travelPackage;

  // Generate background color based on package type
  const getBgColor = () => {
    switch (type.toLowerCase()) {
      case 'religious':
        return 'bg-purple-50';
      case 'thrill':
        return 'bg-orange-50';
      case 'relaxing':
        return 'bg-blue-50';
      default:
        return 'bg-gray-50';
    }
  };

  // Generate accent color based on package type
  const getAccentColor = () => {
    switch (type.toLowerCase()) {
      case 'religious':
        return 'text-purple-700';
      case 'thrill':
        return 'text-orange-700';
      case 'relaxing':
        return 'text-blue-700';
      default:
        return 'text-indigo-700';
    }
  };

  // Generate button color based on package type
  const getButtonColor = () => {
    switch (type.toLowerCase()) {
      case 'religious':
        return 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-500';
      case 'thrill':
        return 'bg-orange-600 hover:bg-orange-700 focus:ring-orange-500';
      case 'relaxing':
        return 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500';
      default:
        return 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500';
    }
  };

  return (
    <div className={`${isSelected ? 'ring-2 ring-offset-2' : ''} ${isSelected && type && type.toLowerCase() === 'religious' ? 'ring-purple-600' : isSelected && type && type.toLowerCase() === 'thrill' ? 'ring-orange-600' : isSelected ? 'ring-blue-600' : ''} bg-white rounded-xl shadow-lg overflow-hidden flex flex-col transition-all duration-300 hover:shadow-2xl`}>
      <div className={`${getBgColor()} p-3 border-b flex items-center justify-between`}>
        <div className="flex items-center">
          <PackageTypeIcon type={type} className={`h-6 w-6 mr-2 ${getAccentColor()}`} />
          <span className={`text-sm font-semibold uppercase ${getAccentColor()}`}>
            {type || 'Custom'} Package
          </span>
        </div>
        {travelPackage.badge && (
          <span className="text-xs bg-white px-2 py-1 rounded-full font-semibold shadow-sm">
            {travelPackage.badge}
          </span>
        )}
      </div>
      
      <div className="p-6 flex-grow">
        <h3 className="text-2xl font-bold text-gray-800 mb-2" style={{ fontFamily: "'Playfair Display', serif"}}>{travelPackage.name}</h3>
        <p className="text-sm text-gray-500 mb-1">Destination: {travelPackage.destination}</p>
        <p className="text-sm text-gray-600 mb-4 h-16 overflow-y-auto">{travelPackage.description}</p>

        {/* Flight Details */}
        <div className="mb-6 border-t border-gray-200 pt-4">
          <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <PlaneIcon className="h-6 w-6 mr-2 text-blue-500" />
            Flight Details
          </h4>
          <div className="space-y-2 text-sm text-gray-700">
            <p><strong className="font-medium">Airline:</strong> {flight.airline}</p>
            <p><strong className="font-medium">Route:</strong> {flight.departureCity} to {flight.arrivalCity}</p>
            <div className="grid grid-cols-2 gap-x-4">
              <p className="flex items-center"><CalendarDaysIcon className="h-4 w-4 mr-1 text-gray-500"/><strong>Out:</strong> {flight.departureDate} <ClockIcon className="h-4 w-4 ml-2 mr-1 text-gray-500"/>{flight.departureTimeOutbound} - {flight.arrivalTimeOutbound}</p>
              <p className="flex items-center"><CalendarDaysIcon className="h-4 w-4 mr-1 text-gray-500"/><strong>Return:</strong> {flight.returnDate} <ClockIcon className="h-4 w-4 ml-2 mr-1 text-gray-500"/>{flight.departureTimeInbound} - {flight.arrivalTimeInbound}</p>
            </div>
            <p><strong className="font-medium">Stops:</strong> {flight.stops}, <strong className="font-medium">Class:</strong> {flight.cabinClass}</p>
            <p className="flex items-center"><BuildingStorefrontIcon className="h-4 w-4 mr-1 text-gray-500"/> <strong className="font-medium">Platform:</strong> {flight.platform}</p>
            <p className="text-md font-semibold text-blue-600"><strong className="font-medium text-gray-700">Price:</strong> ${flight.price?.toLocaleString() || 'N/A'}</p>
          </div>
        </div>

        {/* Hotel Details */}
        <div className="mb-6 border-t border-gray-200 pt-4">
          <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <BedIcon className="h-6 w-6 mr-2 text-green-500" />
            Hotel Details
          </h4>
          <div className="space-y-2 text-sm text-gray-700">
            <p><strong className="font-medium">Name:</strong> {hotel.name} ({hotel.type})</p>
            <div className="flex items-center"><strong className="font-medium mr-2">Rating:</strong> <StarRatingDisplay rating={hotel.starRating} /></div>
            <p><strong className="font-medium">Nights:</strong> {hotel.numberOfNights}</p>
            {hotel.amenities && hotel.amenities.length > 0 && (
              <div>
                <strong className="font-medium">Amenities:</strong>
                <ul className="list-disc list-inside ml-1 flex flex-wrap gap-x-2">
                  {hotel.amenities.slice(0, 4).map(amenity => (
                    <li key={amenity} className="text-xs bg-gray-100 px-2 py-0.5 rounded-full my-0.5 flex items-center">
                      <CheckCircleIcon className="h-3 w-3 mr-1 text-green-500"/>{amenity}
                    </li>
                  ))}
                  {hotel.amenities.length > 4 && <li className="text-xs text-gray-500">+{hotel.amenities.length - 4} more</li>}
                </ul>
              </div>
            )}
            <p className="flex items-center"><BuildingStorefrontIcon className="h-4 w-4 mr-1 text-gray-500"/> <strong className="font-medium">Platform:</strong> {hotel.platform}</p>
             <p className="text-md font-semibold text-green-600"><strong className="font-medium text-gray-700">Price:</strong> ${hotel.pricePerNight?.toLocaleString() || 'N/A'}/night</p>
          </div>
        </div>
        
        {/* Key Highlights */}
        {travelPackage.highlights && travelPackage.highlights.length > 0 && (
          <div className="mb-6 border-t border-gray-200 pt-4">
            <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <StarIcon className="h-6 w-6 mr-2 text-yellow-500" />
              Key Highlights
            </h4>
            <ul className="space-y-1">
              {travelPackage.highlights.map((highlight, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 mr-2 text-green-500 flex-shrink-0" />
                  <span>{highlight}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Information Sources */}
        {sources && sources.length > 0 && (
          <div className="border-t border-gray-200 pt-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
              <InformationCircleIcon className="h-5 w-5 mr-2 text-gray-500" />
              Information Sources
            </h4>
            <ul className="space-y-1 text-xs">
              {sources.map((source, index) => source.web?.uri && source.web?.title && (
                <li key={index} className="flex items-start">
                  <LinkIcon className="h-3 w-3 mr-1.5 text-indigo-500 mt-0.5 flex-shrink-0"/> 
                  <a 
                    href={source.web.uri} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-indigo-600 hover:text-indigo-800 hover:underline break-all"
                    title={source.web.uri}
                  >
                    {source.web.title || source.web.uri}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className={`${getBgColor()} p-6 border-t border-gray-200 mt-auto`}>
        <div className="flex justify-between items-center mb-4">
            <p className={`text-2xl font-bold ${getAccentColor()} flex items-center`}>
                <BanknotesIcon className="h-7 w-7 mr-2 text-gray-500"/> Total:
            </p>
            <p className={`text-3xl font-extrabold ${getAccentColor()}`}>${travelPackage.totalPrice?.toLocaleString() || 'N/A'}</p>
        </div>
        <button
            onClick={() => onSelect(travelPackage)}
            className={`w-full ${getButtonColor()} text-white font-semibold py-3 px-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-opacity-50`}
        >
          {isSelected ? 'Selected Package' : 'Select This Package'}
        </button>
      </div>
    </div>
  );
};

export default PackageCard;
