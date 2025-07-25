import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ItineraryTimeline from '../components/trip/ItineraryTimeline';
import ItineraryMap from '../components/trip/ItineraryMap';
import ChatRefinement from '../components/trip/ChatRefinement';
import apiService from '../services/apiService';

const ItineraryPage = () => {
  const { tripId } = useParams();
  const [itinerary, setItinerary] = useState(null);
  const [tripDetails, setTripDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeDay, setActiveDay] = useState(1);

  useEffect(() => {
    // Fetch real data from the API
    const fetchItinerary = async () => {
      try {
        setLoading(true);
        
        // Get trip details from the API
        const tripResponse = await apiService.getTrip(tripId);
        const tripData = tripResponse.data;
        setTripDetails(tripData);
        
        // Try to get itinerary if it exists
        try {
          const itineraryResponse = await apiService.getItinerary(tripId);
          setItinerary(itineraryResponse.data);
        } catch (err) {
          // If no itinerary exists yet, generate one
          if (err.response && err.response.status === 404) {
            const generatedResponse = await apiService.generateItinerary(tripId);
            setItinerary(generatedResponse.data);
          } else {
            throw err;
          }
        }
      } catch (error) {
        console.error("Error fetching trip data:", error);
        alert("Could not load trip data. Using sample data instead.");
        
        // Fall back to mock data if API fails
        const mockTripDetails = {
          id: tripId,
          origin: { city: 'New York', country: 'USA' },
          destinations: [{ city: 'Paris', country: 'France' }],
          start_date: '2025-07-15',
          end_date: '2025-07-22',
          travelers: { adults: 2, children: 0, infants: 0 },
          budget_level: 'MODERATE',
          transport_type: 'AIR',
          preferences: {
            interests: ['art', 'history', 'food', 'sightseeing']
          }
        };
        
        const mockItinerary = {
          trip_id: tripId,
          ai_generated: true,
          total_cost_estimate: 3500,
          days: [
            {
              day_number: 1,
              date: '2025-07-15',
              activities: [
                {
                  name: 'Eiffel Tower Visit',
                  description: 'Visit the iconic Eiffel Tower and enjoy panoramic views of Paris',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '10:00',
                  end_time: '12:30',
                  cost_estimate: 25.50
                },
                {
                  name: 'Seine River Cruise',
                  description: 'Relaxing cruise along the Seine River to see Paris from a different perspective',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '14:00',
                  end_time: '15:30',
                  cost_estimate: 15.00
                },
                {
                  name: 'Dinner at Le Jules Verne',
                  description: 'Fine dining experience with views of the city',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '19:00',
                  end_time: '21:00',
                  cost_estimate: 200.00
                }
              ],
              meals: [
                {
                  name: 'Breakfast at Hotel',
                  description: 'Continental breakfast',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '08:00',
                  cost_estimate: 0
                },
                {
                  name: 'Lunch at Café de Flore',
                  description: 'Classic Parisian café experience',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '13:00',
                  cost_estimate: 30.00
                }
              ],
              accommodation: {
                name: 'Hotel Paris Center',
                location: { city: 'Paris', country: 'France' },
                check_in_date: '2025-07-15',
                check_out_date: '2025-07-22',
                cost_estimate: 200.00
              }
            },
            {
              day_number: 2,
              date: '2025-07-16',
              activities: [
                {
                  name: 'Louvre Museum',
                  description: 'Explore one of the world\'s largest art museums',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '09:00',
                  end_time: '13:00',
                  cost_estimate: 17.00
                },
                {
                  name: 'Luxembourg Gardens',
                  description: 'Relax in these beautiful gardens',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '14:30',
                  end_time: '16:00',
                  cost_estimate: 0
                },
                {
                  name: 'Shopping at Champs-Élysées',
                  description: 'Shopping at one of the world\'s most famous avenues',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '16:30',
                  end_time: '18:30',
                  cost_estimate: 100.00
                }
              ],
              meals: [
                {
                  name: 'Breakfast at Hotel',
                  description: 'Continental breakfast',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '08:00',
                  cost_estimate: 0
                },
                {
                  name: 'Lunch at Angelina',
                  description: 'Famous for their hot chocolate and pastries',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '13:30',
                  cost_estimate: 25.00
                },
                {
                  name: 'Dinner at Le Comptoir',
                  description: 'Classic French bistro',
                  location: { city: 'Paris', country: 'France' },
                  start_time: '19:30',
                  cost_estimate: 45.00
                }
              ],
              accommodation: {
                name: 'Hotel Paris Center',
                location: { city: 'Paris', country: 'France' },
                check_in_date: '2025-07-15',
                check_out_date: '2025-07-22',
                cost_estimate: 200.00
              }
            }
            // Additional days would be added here in a real application
          ]
        };

        setTripDetails(mockTripDetails);
        setItinerary(mockItinerary);
      } catch (error) {
        console.error('Error fetching itinerary:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchItinerary();
  }, [tripId]);

  const handleDayChange = (dayNumber) => {
    setActiveDay(dayNumber);
  };

  const handleRefinementSubmit = async (request) => {
    try {
      console.log('Refining itinerary with request:', request);
      // In a real app, we would make an API call to refine the itinerary
      
      // For now, just show a success message
      alert('Itinerary refinement request sent! The AI is processing your request.');
      
      // We would then update the itinerary with the response from the API
    } catch (error) {
      console.error('Error refining itinerary:', error);
      alert('Failed to refine itinerary. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!itinerary || !tripDetails) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold text-gray-900">Itinerary Not Found</h2>
        <p className="mt-2 text-gray-600">We couldn't find the itinerary you're looking for.</p>
      </div>
    );
  }

  const currentDayItinerary = itinerary.days.find(day => day.day_number === activeDay) || itinerary.days[0];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Your Trip to {tripDetails.destinations[0].city}, {tripDetails.destinations[0].country}
        </h1>
        <div className="flex flex-wrap gap-2">
          <span className="badge badge-blue">{tripDetails.start_date} - {tripDetails.end_date}</span>
          <span className="badge badge-green">{tripDetails.budget_level}</span>
          <span className="badge badge-purple">{tripDetails.travelers.adults} Adult{tripDetails.travelers.adults > 1 ? 's' : ''}</span>
          {tripDetails.preferences?.interests.map((interest, i) => (
            <span key={i} className="badge badge-blue">{interest}</span>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Left sidebar - Day selector */}
        <div className="md:col-span-1">
          <div className="sticky top-8">
            <div className="card mb-6">
              <div className="card-header">
                <h3 className="text-lg font-semibold">Your {itinerary.days.length}-Day Itinerary</h3>
              </div>
              <div className="card-body p-0">
                <ul className="divide-y divide-gray-200">
                  {itinerary.days.map((day) => (
                    <li key={day.day_number}>
                      <button
                        onClick={() => handleDayChange(day.day_number)}
                        className={`w-full px-4 py-3 text-left hover:bg-gray-50 focus:outline-none ${activeDay === day.day_number ? 'bg-primary-50 border-l-4 border-primary-600' : ''}`}
                      >
                        <div className="flex justify-between items-center">
                          <span className="font-medium">Day {day.day_number}</span>
                          <span className="text-sm text-gray-500">{day.date}</span>
                        </div>
                        <p className="text-sm text-gray-500 mt-1 truncate">
                          {day.activities.length} Activities
                        </p>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold">Trip Summary</h3>
              </div>
              <div className="card-body">
                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Total Budget</p>
                    <p className="text-lg font-semibold">${itinerary.total_cost_estimate.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Duration</p>
                    <p className="text-lg font-semibold">{itinerary.days.length} Days</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Activities</p>
                    <p className="text-lg font-semibold">
                      {itinerary.days.reduce((acc, day) => acc + day.activities.length, 0)} Total
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <div className="md:col-span-2 space-y-8">
          {/* Map */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold">Day {currentDayItinerary.day_number} Map</h3>
            </div>
            <div className="h-80">
              <ItineraryMap day={currentDayItinerary} />
            </div>
          </div>

          {/* Timeline */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold">Day {currentDayItinerary.day_number} Schedule</h3>
              <p className="text-sm text-gray-500">{currentDayItinerary.date}</p>
            </div>
            <div className="card-body">
              <ItineraryTimeline day={currentDayItinerary} />
            </div>
          </div>

          {/* Accommodation */}
          {currentDayItinerary.accommodation && (
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold">Accommodation</h3>
              </div>
              <div className="card-body">
                <h4 className="font-medium text-lg">{currentDayItinerary.accommodation.name}</h4>
                <p className="text-gray-600">
                  {currentDayItinerary.accommodation.location.city}, {currentDayItinerary.accommodation.location.country}
                </p>
                {currentDayItinerary.accommodation.cost_estimate && (
                  <p className="text-sm text-gray-500 mt-2">
                    Estimated cost: ${currentDayItinerary.accommodation.cost_estimate.toFixed(2)}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Refinement Chat */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold">Refine Your Itinerary</h3>
              <p className="text-sm text-gray-500">
                Ask our AI to make changes to your itinerary
              </p>
            </div>
            <div className="card-body">
              <ChatRefinement onSubmit={handleRefinementSubmit} currentDay={activeDay} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItineraryPage;
