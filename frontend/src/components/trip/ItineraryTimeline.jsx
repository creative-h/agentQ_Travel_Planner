import React from 'react';

const ItineraryTimeline = ({ day }) => {
  // Combine all day events (activities and meals) and sort by time
  const allEvents = [...(day.activities || []), ...(day.meals || [])].sort((a, b) => {
    if (!a.start_time) return 1;
    if (!b.start_time) return -1;
    return a.start_time.localeCompare(b.start_time);
  });

  return (
    <div className="relative pl-8">
      {/* Timeline line */}
      <div className="timeline-line"></div>
      
      {/* Timeline items */}
      <div className="space-y-8">
        {allEvents.map((event, index) => {
          const isActivity = day.activities.includes(event);
          // eventType variable removed to fix build warning

          return (
            <div key={index} className="relative">
              {/* Timeline dot */}
              <div className={`timeline-dot ${isActivity ? 'bg-primary-600' : 'bg-secondary-500'}`}></div>
              
              <div className="ml-6">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">{event.name}</h4>
                    <p className="text-sm text-gray-500">
                      {event.start_time && (
                        <span>{event.start_time}{event.end_time && ` - ${event.end_time}`}</span>
                      )}
                    </p>
                  </div>
                  <span className={`badge ${isActivity ? 'badge-blue' : 'badge-green'}`}>
                    {isActivity ? 'Activity' : 'Meal'}
                  </span>
                </div>
                
                <p className="mt-2 text-gray-600">{event.description}</p>
                
                {event.location && (
                  <p className="mt-1 text-sm text-gray-500">
                    {event.location.city}, {event.location.country}
                  </p>
                )}
                
                {event.cost_estimate !== undefined && event.cost_estimate > 0 && (
                  <p className="mt-2 text-sm font-medium">
                    Estimated cost: ${event.cost_estimate.toFixed(2)}
                  </p>
                )}
                
                <div className="mt-4 flex space-x-3">
                  <button className="text-sm font-medium text-primary-600 hover:text-primary-800">
                    Edit
                  </button>
                  <button className="text-sm font-medium text-gray-500 hover:text-gray-700">
                    Replace
                  </button>
                  <button className="text-sm font-medium text-red-600 hover:text-red-800">
                    Delete
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        
        {/* Add activity button */}
        <div className="relative">
          <div className="timeline-dot bg-gray-300"></div>
          <div className="ml-6">
            <button className="flex items-center text-primary-600 hover:text-primary-800">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Activity
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItineraryTimeline;
