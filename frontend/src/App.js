import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import NewTripPage from './routes/NewTripPage';
import ItineraryPage from './routes/ItineraryPage';
import NotFoundPage from './routes/NotFoundPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/trips/new" replace />} />
        <Route path="trips/new" element={<NewTripPage />} />
        <Route path="trips/:tripId/itinerary" element={<ItineraryPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
