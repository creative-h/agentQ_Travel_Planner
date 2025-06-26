import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

// Custom icons for different types of locations
const createIcon = (color) => {
  return new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
};

const activityIcon = createIcon('blue');
const mealIcon = createIcon('green');
const accommodationIcon = createIcon('red');

const ItineraryMap = ({ day }) => {
  // Combine all locations from day's activities, meals, and accommodation
  const locations = [];

  // Add activities
  if (day.activities) {
    day.activities.forEach((activity) => {
      if (activity.location) {
        locations.push({
          ...activity,
          type: 'activity',
          icon: activityIcon
        });
      }
    });
  }

  // Add meals
  if (day.meals) {
    day.meals.forEach((meal) => {
      if (meal.location) {
        locations.push({
          ...meal,
          type: 'meal',
          icon: mealIcon
        });
      }
    });
  }

  // Add accommodation
  if (day.accommodation && day.accommodation.location) {
    locations.push({
      ...day.accommodation,
      type: 'accommodation',
      icon: accommodationIcon
    });
  }

  // For demo purposes, use fixed coordinates for Paris if no real coordinates
  const defaultCenter = [48.8566, 2.3522]; // Paris
  
  // Try to get center from the first location with coordinates
  let mapCenter = defaultCenter;
  let mapZoom = 13;

  // In a real app, the locations would have actual coordinates
  // For demo, we'll create some fake coordinates near Paris for the locations
  const withCoordinates = locations.map((location, index) => {
    // Generate some coordinates around Paris with small offsets
    const lat = 48.8566 + (Math.random() - 0.5) * 0.05;
    const lng = 2.3522 + (Math.random() - 0.5) * 0.05;
    
    return {
      ...location,
      coordinates: { lat, lng }
    };
  });

  return (
    <MapContainer center={mapCenter} zoom={mapZoom} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {withCoordinates.map((item, index) => (
        <Marker 
          key={index} 
          position={[item.coordinates.lat, item.coordinates.lng]}
          icon={item.icon}
        >
          <Popup>
            <div>
              <h3 className="font-medium">{item.name}</h3>
              <p className="text-sm">{item.description}</p>
              {item.start_time && (
                <p className="text-xs mt-1">
                  {item.start_time}{item.end_time ? ` - ${item.end_time}` : ''}
                </p>
              )}
              <p className="text-xs mt-1">
                {item.type.charAt(0).toUpperCase() + item.type.slice(1)}
              </p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default ItineraryMap;
