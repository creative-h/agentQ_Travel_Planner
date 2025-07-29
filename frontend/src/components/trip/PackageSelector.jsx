import React, { useState, useEffect } from 'react';
import PackageCard from './PackageCard';
import { PACKAGE_TYPES } from '../../types';

const PackageSelector = ({ itinerary, tripDetails, onSelectPackage }) => {
  const [packages, setPackages] = useState([]);
  
  // Generate package recommendations based on trip details and itinerary
  useEffect(() => {
    if (!itinerary || !tripDetails) return;
    
    const destination = tripDetails.destinations[0].city;
    const duration = itinerary.days.length;
    const start = tripDetails.start_date;
    const end = tripDetails.end_date;
    const budgetLevel = tripDetails.budget_level;
    
    // Calculate estimated costs based on budget level
    const flightCostBase = budgetLevel === 'luxury' ? 1200 : budgetLevel === 'moderate' ? 800 : 500;
    const hotelCostBase = budgetLevel === 'luxury' ? 350 : budgetLevel === 'moderate' ? 180 : 80;
    
    // Create packages with different focuses
    const generatedPackages = [
      {
        id: 1,
        type: PACKAGE_TYPES.RELIGIOUS,
        name: `Spiritual ${destination} Experience`,
        destination: `${destination}, ${tripDetails.destinations[0].country}`,
        description: `Discover the spiritual heritage of ${destination} with visits to historic temples, churches, and sacred sites. This package focuses on cultural immersion and spiritual rejuvenation.`,
        totalPrice: Math.round((flightCostBase + (hotelCostBase * duration)) * 1.1),
        badge: 'Cultural Heritage',
        highlights: [
          'Guided tours of religious monuments',
          'Meeting with local spiritual leaders',
          'Traditional ceremonies participation',
          'Sacred site meditation sessions',
          'Religious art and architecture tours'
        ],
        flight: {
          airline: 'Spiritual Airways',
          departureCity: tripDetails.origin.city,
          arrivalCity: destination,
          departureDate: start,
          returnDate: end,
          departureTimeOutbound: '07:30',
          arrivalTimeOutbound: '10:45',
          departureTimeInbound: '18:30',
          arrivalTimeInbound: '21:45',
          stops: 'Non-stop',
          cabinClass: budgetLevel === 'luxury' ? 'Business' : 'Economy',
          platform: 'SacredTravels.com',
          price: flightCostBase
        },
        hotel: {
          name: `${destination} Heritage Hotel`,
          type: 'Historic Property',
          starRating: budgetLevel === 'luxury' ? 5 : budgetLevel === 'moderate' ? 4 : 3,
          numberOfNights: duration,
          platform: 'SpiritStays.com',
          pricePerNight: hotelCostBase,
          amenities: ['Temple View', 'Meditation Garden', 'Spiritual Library', 'Prayer Room', 'Cultural Activities', 'Vegetarian Restaurant']
        },
        sources: [
          { web: { uri: 'https://example.com/religious-tourism', title: 'Religious Tourism Guide' } },
          { web: { uri: 'https://example.com/sacred-sites', title: `Sacred Sites of ${destination}` } }
        ]
      },
      {
        id: 2,
        type: PACKAGE_TYPES.THRILL,
        name: `${destination} Adventure Package`,
        destination: `${destination}, ${tripDetails.destinations[0].country}`,
        description: `Experience the ultimate adrenaline rush in ${destination}. This package combines extreme sports, adventure tours, and high-energy activities for the thrill-seeker.`,
        totalPrice: Math.round((flightCostBase + (hotelCostBase * duration)) * 1.15),
        badge: 'Adrenaline Rush',
        highlights: [
          'Extreme sports and activities',
          'Adventure hiking expeditions',
          'Water sports and rafting',
          'Rock climbing and rappelling',
          'Guided off-road explorations'
        ],
        flight: {
          airline: 'Adventure Airlines',
          departureCity: tripDetails.origin.city,
          arrivalCity: destination,
          departureDate: start,
          returnDate: end,
          departureTimeOutbound: '06:15',
          arrivalTimeOutbound: '09:30',
          departureTimeInbound: '19:45',
          arrivalTimeInbound: '23:00',
          stops: 'Non-stop',
          cabinClass: budgetLevel === 'luxury' ? 'Premium Economy' : 'Economy',
          platform: 'ThrillTickets.com',
          price: flightCostBase + 50
        },
        hotel: {
          name: `${destination} Adventure Lodge`,
          type: 'Activity Resort',
          starRating: budgetLevel === 'luxury' ? 4.5 : budgetLevel === 'moderate' ? 4 : 3,
          numberOfNights: duration,
          platform: 'AdventureLodging.com',
          pricePerNight: hotelCostBase + 20,
          amenities: ['Equipment Rental', 'Adventure Tours Desk', 'Climbing Wall', 'Mountain Views', 'Expedition Planning', 'Sports Bar']
        },
        sources: [
          { web: { uri: 'https://example.com/adventure-travel', title: 'Adventure Travel Guide' } },
          { web: { uri: 'https://example.com/extreme-activities', title: `Extreme Activities in ${destination}` } }
        ]
      },
      {
        id: 3,
        type: PACKAGE_TYPES.RELAXING,
        name: `${destination} Relaxation Retreat`,
        destination: `${destination}, ${tripDetails.destinations[0].country}`,
        description: `Unwind and rejuvenate in the tranquil settings of ${destination}. This package focuses on wellness, relaxation, and self-care with premium spa services and peaceful accommodations.`,
        totalPrice: Math.round((flightCostBase + (hotelCostBase * duration)) * 1.2),
        badge: 'Wellness & Spa',
        highlights: [
          'Daily spa treatments included',
          'Wellness and meditation sessions',
          'Gourmet healthy dining options',
          'Scenic nature walks and yoga',
          'Personalized relaxation program'
        ],
        flight: {
          airline: 'Tranquil Air',
          departureCity: tripDetails.origin.city,
          arrivalCity: destination,
          departureDate: start,
          returnDate: end,
          departureTimeOutbound: '09:00',
          arrivalTimeOutbound: '12:15',
          departureTimeInbound: '16:30',
          arrivalTimeInbound: '19:45',
          stops: 'Non-stop',
          cabinClass: budgetLevel === 'luxury' ? 'First Class' : budgetLevel === 'moderate' ? 'Business' : 'Premium Economy',
          platform: 'RelaxJourneys.com',
          price: flightCostBase + 100
        },
        hotel: {
          name: `${destination} Wellness Spa & Resort`,
          type: 'Luxury Spa Resort',
          starRating: budgetLevel === 'luxury' ? 5 : budgetLevel === 'moderate' ? 4.5 : 4,
          numberOfNights: duration,
          platform: 'WellnessRetreats.com',
          pricePerNight: hotelCostBase + 50,
          amenities: ['Spa Access', 'Hot Springs', 'Wellness Center', 'Infinity Pool', 'Meditation Classes', 'Gourmet Restaurant', 'Private Beach Access']
        },
        sources: [
          { web: { uri: 'https://example.com/wellness-travel', title: 'Wellness Travel Guide' } },
          { web: { uri: 'https://example.com/spa-resorts', title: `Top Spa Resorts in ${destination}` } }
        ]
      }
    ];
    
    setPackages(generatedPackages);
  }, [itinerary, tripDetails]);
  
  if (packages.length === 0) {
    return (
      <div className="animate-pulse bg-gray-100 p-6 rounded-lg">
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6 mb-6"></div>
        <div className="grid grid-cols-1 gap-4">
          <div className="h-64 bg-gray-200 rounded"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Recommended Travel Packages</h2>
      <p className="text-gray-600 mb-6">Choose a package that fits your travel style. Each option offers a unique experience tailored to different preferences.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {packages.map(pkg => (
          <PackageCard 
            key={pkg.id} 
            travelPackage={pkg} 
            onSelect={onSelectPackage} 
          />
        ))}
      </div>
    </div>
  );
};

export default PackageSelector;
