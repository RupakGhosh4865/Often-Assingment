# Travel Itinerary Management System

A backend system for managing travel itineraries in Thailand (Phuket and Krabi regions) with FastAPI and SQLAlchemy.

## Features

- Database architecture for trip itineraries using SQLAlchemy
- RESTful API endpoints for creating and viewing itineraries
- MCP server for recommended itineraries based on duration
- Sample data for Phuket and Krabi regions

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

1. Create Itinerary
   - POST `/itineraries/`
   - Creates a new trip itinerary

2. List Itineraries
   - GET `/itineraries/`
   - Returns a list of all itineraries

3. Get Itinerary
   - GET `/itineraries/{itinerary_id}`
   - Returns details of a specific itinerary

4. Get Recommended Itineraries
   - GET `/recommended-itineraries/{nights}`
   - Returns recommended itineraries for a specific duration

5. MCP Recommendations
   - POST `/mcp/recommendations/`
   - Returns recommended itineraries based on duration

## Database Schema

The system uses the following main entities:
- Location (cities, attractions, hotels)
- Itinerary (trip plans)
- ItineraryDay (day-wise planning)
- Activity (excursions and activities)
- Transfer (transportation between locations)

## Sample Data

The system comes with pre-populated sample data for:
- Popular locations in Phuket and Krabi
- Sample itineraries ranging from 3-5 nights
- Various activities and transfers

To seed the database with sample data, run:
```bash
python -m app.seed_data
``` 