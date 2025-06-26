from fastapi.testclient import TestClient
import pytest
from datetime import date, timedelta

from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_trip():
    """Test creating a new trip"""
    # Create test data
    tomorrow = date.today() + timedelta(days=1)
    next_week = date.today() + timedelta(days=7)
    
    trip_data = {
        "origin": {"city": "New York", "country": "USA"},
        "destinations": [{"city": "Paris", "country": "France"}],
        "start_date": tomorrow.isoformat(),
        "end_date": next_week.isoformat(),
        "travelers": {"adults": 2, "children": 1, "infants": 0},
        "budget_level": "MODERATE",
        "transport_type": "AIR"
    }
    
    # Send request to create trip
    response = client.post("/v1/trips/", json=trip_data)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["origin"]["city"] == "New York"
    assert len(data["destinations"]) == 1
    assert data["destinations"][0]["city"] == "Paris"
