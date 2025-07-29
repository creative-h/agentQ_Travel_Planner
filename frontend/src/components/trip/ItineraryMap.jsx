import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
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
  const [mapCenter, setMapCenter] = useState([48.8566, 2.3522]); // Default to Paris
  const [mapLocations, setMapLocations] = useState([]);
  const [routePoints, setRoutePoints] = useState([]);
  const [cityCoordinates, setCityCoordinates] = useState({});
  
  // Helper function to get coordinates for a city (simulated)
  const getCoordinatesForCity = (city, country) => {
    // In a real app, we would use a geocoding API
    // This is a simplified version with some hardcoded coordinates for common cities
    const cityMap = {
      'paris': [48.8566, 2.3522],
      'london': [51.5074, -0.1278],
      'new york': [40.7128, -74.0060],
      'tokyo': [35.6762, 139.6503],
      'rome': [41.9028, 12.4964],
      'barcelona': [41.3851, 2.1734],
      'dubai': [25.2048, 55.2708],
      'sydney': [-33.8688, 151.2093],
      'berlin': [52.5200, 13.4050],
      'amsterdam': [52.3676, 4.9041],
      'madrid': [40.4168, -3.7038],
      'vienna': [48.2082, 16.3738],
      'prague': [50.0755, 14.4378],
      'lisbon': [38.7223, -9.1393],
      'florence': [43.7696, 11.2558],
      'venice': [45.4408, 12.3155],
      'milan': [45.4642, 9.1900],
      'cairo': [30.0444, 31.2357],
      'marrakech': [31.6295, -7.9811],
      'bangkok': [13.7563, 100.5018],
      'singapore': [1.3521, 103.8198],
      'delhi': [28.6139, 77.2090],
      'mumbai': [19.0760, 72.8777],
      'beijing': [39.9042, 116.4074],
      'shanghai': [31.2304, 121.4737],
      'seoul': [37.5665, 126.9780],
      'istanbul': [41.0082, 28.9784],
      'rio de janeiro': [-22.9068, -43.1729],
      'buenos aires': [-34.6037, -58.3816],
      'mexico city': [19.4326, -99.1332],
      'los angeles': [34.0522, -118.2437],
      'san francisco': [37.7749, -122.4194],
      'chicago': [41.8781, -87.6298],
      'toronto': [43.6532, -79.3832],
      'montreal': [45.5017, -73.5673],
      'vancouver': [49.2827, -123.1207],
      // Default for cities we don't have coordinates for
      'default': [0, 0]
    };
    
    const key = city.toLowerCase();
    return cityMap[key] || cityMap['default'];
  };

  useEffect(() => {
    // Process locations from day data
    const locations = [];
    const routeCoordinates = [];
    const cityCoords = {};
    
    // Process accommodation first as main base
    if (day.accommodation && day.accommodation.location) {
      const city = day.accommodation.location.city;
      const country = day.accommodation.location.country;
      const coords = getCoordinatesForCity(city, country);
      
      cityCoords[city.toLowerCase()] = coords;
      
      locations.push({
        ...day.accommodation,
        type: 'accommodation',
        icon: accommodationIcon,
        position: coords
      });
      
      // Set map center to accommodation location
      setMapCenter(coords);
    }
    
    // Process activities
    if (day.activities) {
      day.activities.forEach((activity, index) => {
        if (activity.location) {
          const city = activity.location.city;
          const country = activity.location.country;
          
          // Check if we already have coordinates for this city
          let coords;
          if (cityCoords[city.toLowerCase()]) {
            // Slightly offset coordinates for items in the same city
            coords = [
              cityCoords[city.toLowerCase()][0] + (Math.random() - 0.5) * 0.01, 
              cityCoords[city.toLowerCase()][1] + (Math.random() - 0.5) * 0.01
            ];
          } else {
            coords = getCoordinatesForCity(city, country);
            cityCoords[city.toLowerCase()] = coords;
          }
          
          locations.push({
            ...activity,
            type: 'activity',
            icon: activityIcon,
            position: coords
          });
          
          routeCoordinates.push(coords);
        }
      });
    }
    
    // Process meals
    if (day.meals) {
      day.meals.forEach((meal) => {
        if (meal.location) {
          const city = meal.location.city;
          const country = meal.location.country;
          
          // Check if we already have coordinates for this city
          let coords;
          if (cityCoords[city.toLowerCase()]) {
            // Slightly offset coordinates for items in the same city
            coords = [
              cityCoords[city.toLowerCase()][0] + (Math.random() - 0.5) * 0.01, 
              cityCoords[city.toLowerCase()][1] + (Math.random() - 0.5) * 0.01
            ];
          } else {
            coords = getCoordinatesForCity(city, country);
            cityCoords[city.toLowerCase()] = coords;
          }
          
          locations.push({
            ...meal,
            type: 'meal',
            icon: mealIcon,
            position: coords
          });
        }
      });
    }

    setMapLocations(locations);
    setRoutePoints(routeCoordinates);
    setCityCoordinates(cityCoords);
  }, [day]);

  // If no locations, show a placeholder
  if (mapLocations.length === 0) {
    return (
      <div className="flex justify-center items-center h-full bg-gray-100">
        <p className="text-gray-500">No locations to display for this day.</p>
      </div>
    );
  }

  return (
    <MapContainer
      center={mapCenter}
      zoom={13}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      {/* Display markers for all locations */}
      {mapLocations.map((location, index) => (
        <Marker 
          key={`${location.type}-${index}`} 
          position={location.position} 
          icon={location.icon}
        >
          <Popup>
            <div className="font-medium">{location.name}</div>
            {location.description && (
              <div className="text-sm">{location.description}</div>
            )}
            {location.cost_estimate && (
              <div className="text-sm font-semibold mt-1">
                Cost: ${location.cost_estimate.toFixed(2)}
              </div>
            )}
            {location.start_time && location.end_time && (
              <div className="text-xs text-gray-600 mt-1">
                {location.start_time} - {location.end_time}
              </div>
            )}
          </Popup>
        </Marker>
      ))}
      
      {/* Display route line connecting activity points */}
      {routePoints.length > 1 && (
        <Polyline 
          positions={routePoints}
          color="#3B82F6"
          weight={3}
          opacity={0.7}
          dashArray="5, 10"
        />
      )}
    </MapContainer>
  );
};

export default ItineraryMap;
