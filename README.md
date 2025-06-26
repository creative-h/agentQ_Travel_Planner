# TriprTrek - AI-Powered Travel Planner

## Overview

TriprTrek is an AI-enhanced travel planning application that helps users create personalized trip itineraries. The application uses LLM technology (Groq's LLaMa 3) for natural language processing and travel APIs to generate tailored travel plans based on user preferences.

## Features

- **Trip Initialization**: Select origin/destination, travel dates, number of travelers, budget level, and transportation type
- **Preference Collection**: Input interests, accommodation preferences, dining preferences, and special requirements
- **AI-Powered Itinerary Generation**: Using LLaMa 3 to create personalized day-by-day itineraries
- **Interactive Itinerary Viewer**: Timeline and map-based visualization of trip activities
- **Natural Language Refinement**: Chat-based interface for making changes to the itinerary

## Project Structure

The project follows a clean, modular architecture with separate frontend and backend components:

```
/newTrip
├── /backend                 # FastAPI backend
│   ├── /app
│   │   ├── /api             # API routes and endpoints
│   │   ├── /models          # Database models
│   │   ├── /schemas         # Pydantic schemas for validation
│   │   ├── /services        # Business logic services
│   │   ├── /utils           # Utility functions
│   │   └── /config          # Configuration management
│   ├── /logs                # Application logs
│   └── requirements.txt     # Python dependencies
│
└── /frontend                # React frontend
    ├── /public              # Static assets
    └── /src
        ├── /components      # Reusable UI components
        │   ├── /trip        # Trip-specific components
        │   └── /ui          # Generic UI components
        ├── /services        # API service interactions
        ├── /hooks           # Custom React hooks
        ├── /utils           # Utility functions
        ├── /store           # State management
        └── /routes          # Application routes
```

## Technology Stack

### Backend
- **Language**: Python
- **Framework**: FastAPI
- **AI Integration**: Groq API (LLaMa 3)
- **Travel API**: Amadeus (simulated in demo)
- **Database**: PostgreSQL (configured, not implemented in demo)

### Frontend
- **Framework**: React
- **Styling**: TailwindCSS
- **State Management**: React hooks
- **Routing**: React Router
- **Maps**: Leaflet
- **Form Handling**: React Hook Form

## Setup Instructions

### Backend Setup

1. Activate the virtual environment:
   ```bash
   source /home/lubuntu/myenv/bin/activate
   ```

2. Install dependencies:
   ```bash
   cd /home/lubuntu/Downloads/tripyTrek/newTrip/backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the backend directory based on the existing template
   - Add your API keys for Groq and Amadeus

4. Run the FastAPI server:
   ```bash
   cd /home/lubuntu/Downloads/tripyTrek/newTrip/backend
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Install npm dependencies:
   ```bash
   cd /home/lubuntu/Downloads/tripyTrek/newTrip/frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## API Documentation

Once the backend server is running, you can access the auto-generated API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Best Practices

This project follows several best practices:

- **Single Responsibility Principle**: Each module has a single responsibility
- **Clean Code**: Meaningful naming, consistent formatting, and comments
- **Modularity**: Components are reusable and decoupled
- **Error Handling**: Comprehensive error handling with structured logging
- **API Design**: RESTful API design with standardized responses
- **Validation**: Input validation using Pydantic schemas
- **Testing**: Unit and integration test setup (test files created but implementation is minimal)

## Future Enhancements

- Add authentication and user profiles
- Implement persistent storage with PostgreSQL
- Integrate with real travel APIs (Amadeus, Booking.com, etc.)
- Add collaborative planning features
- Implement offline mode and PWA capabilities
- Add sharing features for itineraries
