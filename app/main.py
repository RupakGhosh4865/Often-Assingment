from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Itinerary API")

@app.post("/itineraries/", response_model=schemas.Itinerary)
def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    db_itinerary = models.Itinerary(
        name=itinerary.name,
        duration_nights=itinerary.duration_nights,
        description=itinerary.description,
        is_recommended=itinerary.is_recommended
    )
    db.add(db_itinerary)
    db.flush()

    for day in itinerary.days:
        db_day = models.ItineraryDay(
            itinerary_id=db_itinerary.id,
            day_number=day.day_number,
            hotel_id=day.hotel_id
        )
        db.add(db_day)
        db.flush()

        for activity in day.activities:
            db_activity = models.Activity(
                day_id=db_day.id,
                location_id=activity.location_id,
                name=activity.name,
                description=activity.description,
                start_time=activity.start_time,
                duration_minutes=activity.duration_minutes
            )
            db.add(db_activity)

        for transfer in day.transfers:
            db_transfer = models.Transfer(
                day_id=db_day.id,
                from_location_id=transfer.from_location_id,
                to_location_id=transfer.to_location_id,
                transport_type=transfer.transport_type,
                departure_time=transfer.departure_time,
                duration_minutes=transfer.duration_minutes
            )
            db.add(db_transfer)

    db.commit()
    db.refresh(db_itinerary)
    return db_itinerary

@app.get("/itineraries/", response_model=List[schemas.Itinerary])
def get_itineraries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    itineraries = db.query(models.Itinerary).offset(skip).limit(limit).all()
    return itineraries

@app.get("/itineraries/{itinerary_id}", response_model=schemas.Itinerary)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if itinerary is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary

@app.get("/recommended-itineraries/{nights}", response_model=List[schemas.Itinerary])
def get_recommended_itineraries(nights: int, db: Session = Depends(get_db)):
    itineraries = db.query(models.Itinerary).filter(
        models.Itinerary.duration_nights == nights,
        models.Itinerary.is_recommended == True
    ).all()
    return itineraries

# MCP Server endpoint
@app.post("/mcp/recommendations/", response_model=List[schemas.Itinerary])
def get_mcp_recommendations(request: schemas.ItineraryRecommendation, db: Session = Depends(get_db)):
    recommended_itineraries = db.query(models.Itinerary).filter(
        models.Itinerary.duration_nights == request.duration_nights,
        models.Itinerary.is_recommended == True
    ).all()
    return recommended_itineraries 