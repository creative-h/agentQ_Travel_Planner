import React, { useState } from 'react';
import ChatRefinement from './ChatRefinement';
import { ClockIcon, BuildingStorefrontIcon, BedIcon } from '../icons';

const DayDetails = ({ day, onUpdateDay }) => {
  const [showChat, setShowChat] = useState(false);
  
  const handleRefinementSubmit = async (request) => {
    try {
      // Call the parent component's update function
      const result = await onUpdateDay(request);
      // Hide chat after successful submission
      if (result.success) {
        setTimeout(() => setShowChat(false), 2000);
      }
      return result;
    } catch (error) {
      console.error('Error in day refinement:', error);
      throw error;
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="bg-indigo-600 p-5 text-white">
        <h2 className="text-2xl font-bold mb-1">Day {day.day_number} - {day.date}</h2>
        <p className="text-indigo-100">{day.notes || `Explore and enjoy ${day.activities[0]?.location.city || 'your destination'}`}</p>
      </div>
      
      <div className="p-6">
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Day Summary</h3>
          <div className="bg-gray-50 p-4 rounded-lg">
            <ul className="space-y-3">
              <li className="flex items-start">
                <div className="bg-blue-100 p-2 rounded-full mr-3">
                  <ClockIcon className="h-5 w-5 text-blue-700" />
                </div>
                <div>
                  <p className="font-medium text-gray-800">Activities</p>
                  <p className="text-gray-600">{day.activities.length} planned activities</p>
                </div>
              </li>
              {day.meals && day.meals.length > 0 && (
                <li className="flex items-start">
                  <div className="bg-green-100 p-2 rounded-full mr-3">
                    <BuildingStorefrontIcon className="h-5 w-5 text-green-700" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">Meals</p>
                    <p className="text-gray-600">{day.meals.length} meals included</p>
                  </div>
                </li>
              )}
              {day.accommodation && (
                <li className="flex items-start">
                  <div className="bg-purple-100 p-2 rounded-full mr-3">
                    <BedIcon className="h-5 w-5 text-purple-700" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">Accommodation</p>
                    <p className="text-gray-600">{day.accommodation.name} in {day.accommodation.location.city}</p>
                  </div>
                </li>
              )}
            </ul>
          </div>
        </div>
        
        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-800">Detailed Schedule</h3>
            <button 
              onClick={() => setShowChat(!showChat)}
              className="bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              {showChat ? 'Hide Refinement' : 'Refine This Day'}
            </button>
          </div>
          
          <div className="space-y-6">
            {day.transportation && day.transportation.length > 0 && (
              <div>
                <h4 className="text-lg font-medium text-gray-800 mb-2">Transportation</h4>
                <ul className="space-y-3">
                  {day.transportation.map((transport, idx) => (
                    <li key={idx} className="bg-blue-50 p-3 rounded-lg">
                      <div className="flex justify-between">
                        <span className="font-medium">{transport.type}</span>
                        <span className="text-gray-600">${transport.cost_estimate?.toFixed(2) || '0.00'}</span>
                      </div>
                      <div className="mt-1 text-sm">
                        <div>From: {transport.departure_location.city}, {transport.departure_time}</div>
                        <div>To: {transport.arrival_location.city}, {transport.arrival_time}</div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <div>
              <h4 className="text-lg font-medium text-gray-800 mb-2">Activities</h4>
              <ul className="space-y-3">
                {day.activities.map((activity, idx) => (
                  <li key={idx} className="bg-green-50 p-3 rounded-lg">
                    <div className="flex justify-between">
                      <span className="font-medium">{activity.name}</span>
                      <span className="text-gray-600">${activity.cost_estimate?.toFixed(2) || '0.00'}</span>
                    </div>
                    <div className="mt-1 text-sm text-gray-700">{activity.description}</div>
                    <div className="mt-2 text-sm text-gray-500">
                      {activity.start_time} - {activity.end_time} | {activity.location.city}, {activity.location.country}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            
            {day.meals && day.meals.length > 0 && (
              <div>
                <h4 className="text-lg font-medium text-gray-800 mb-2">Meals</h4>
                <ul className="space-y-3">
                  {day.meals.map((meal, idx) => (
                    <li key={idx} className="bg-yellow-50 p-3 rounded-lg">
                      <div className="flex justify-between">
                        <span className="font-medium">{meal.name}</span>
                        <span className="text-gray-600">${meal.cost_estimate?.toFixed(2) || '0.00'}</span>
                      </div>
                      <div className="mt-1 text-sm text-gray-700">{meal.description}</div>
                      <div className="mt-2 text-sm text-gray-500">
                        {meal.start_time} | {meal.location.city}, {meal.location.country}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {day.accommodation && (
              <div>
                <h4 className="text-lg font-medium text-gray-800 mb-2">Accommodation</h4>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <div className="flex justify-between">
                    <span className="font-medium">{day.accommodation.name}</span>
                    <span className="text-gray-600">${day.accommodation.cost_estimate?.toFixed(2) || '0.00'}/night</span>
                  </div>
                  <div className="mt-2 text-sm text-gray-500">
                    {day.accommodation.location.city}, {day.accommodation.location.country}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {showChat && (
          <div className="mt-6 border-t border-gray-200 pt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Refine Day {day.day_number}</h3>
            <ChatRefinement onSubmit={handleRefinementSubmit} currentDay={day.day_number} />
          </div>
        )}
      </div>
    </div>
  );
};

export default DayDetails;
