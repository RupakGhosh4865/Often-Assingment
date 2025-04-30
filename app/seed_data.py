from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine
from .models import LocationType

def seed_data():
    db = SessionLocal()
    
    # Create locations for Phuket
    phuket_locations = [
        {
            "name": "Patong Beach",
            "type": LocationType.ATTRACTION,
            "description": "Famous beach known for nightlife and water activities",
            "latitude": 7.9016,
            "longitude": 98.2987,
            "region": "Phuket"
        },
        {
            "name": "Hilton Phuket Arcadia",
            "type": LocationType.HOTEL,
            "description": "5-star resort with multiple pools and beachfront access",
            "latitude": 7.8839,
            "longitude": 98.2870,
            "region": "Phuket"
        },
        {
            "name": "Big Buddha Phuket",
            "type": LocationType.ATTRACTION,
            "description": "Famous 45m tall white marble statue",
            "latitude": 7.8276,
            "longitude": 98.3116,
            "region": "Phuket"
        }
    ]

    # Create locations for Krabi
    krabi_locations = [
        {
            "name": "Railay Beach",
            "type": LocationType.ATTRACTION,
            "description": "Beautiful beach accessible only by boat",
            "latitude": 8.0055,
            "longitude": 98.8372,
            "region": "Krabi"
        },
        {
            "name": "Centara Grand Beach Resort",
            "type": LocationType.HOTEL,
            "description": "Luxury resort with private beach access",
            "latitude": 8.0060,
            "longitude": 98.8377,
            "region": "Krabi"
        },
        {
            "name": "Tiger Cave Temple",
            "type": LocationType.ATTRACTION,
            "description": "Buddhist temple complex with 1,237 steps to summit",
            "latitude": 8.1267,
            "longitude": 98.9242,
            "region": "Krabi"
        }
    ]

    # Add locations to database
    for location_data in phuket_locations + krabi_locations:
        location = models.Location(**location_data)
        db.add(location)
    
    db.commit()

    # Create sample itineraries
    # 3-night Phuket itinerary
    phuket_3_night = models.Itinerary(
        name="Phuket Beach Escape",
        duration_nights=3,
        description="A relaxing 3-night beach getaway in Phuket",
        is_recommended=True
    )
    db.add(phuket_3_night)
    db.flush()

    # Add days to Phuket itinerary
    for day_num in range(1, 4):
        day = models.ItineraryDay(
            itinerary_id=phuket_3_night.id,
            day_number=day_num,
            hotel_id=2  # Hilton Phuket
        )
        db.add(day)
        db.flush()

        # Add activities
        activity = models.Activity(
            day_id=day.id,
            location_id=1,  # Patong Beach
            name=f"Beach Day {day_num}",
            description="Relax on the beach and enjoy water activities",
            start_time="10:00",
            duration_minutes=240
        )
        db.add(activity)

    # 5-night Krabi itinerary
    krabi_5_night = models.Itinerary(
        name="Krabi Adventure",
        duration_nights=5,
        description="5 nights of adventure and relaxation in Krabi",
        is_recommended=True
    )
    db.add(krabi_5_night)
    db.flush()

    # Add days to Krabi itinerary
    for day_num in range(1, 6):
        day = models.ItineraryDay(
            itinerary_id=krabi_5_night.id,
            day_number=day_num,
            hotel_id=5  # Centara Grand
        )
        db.add(day)
        db.flush()

        # Add activities
        activity = models.Activity(
            day_id=day.id,
            location_id=4,  # Railay Beach
            name=f"Railay Beach Day {day_num}",
            description="Explore the stunning Railay Beach",
            start_time="09:00",
            duration_minutes=300
        )
        db.add(activity)

    db.commit()
    db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    seed_data() 