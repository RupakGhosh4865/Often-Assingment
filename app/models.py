from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import enum

class LocationType(enum.Enum):
    CITY = "city"
    ATTRACTION = "attraction"
    HOTEL = "hotel"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(LocationType))
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    region = Column(String, index=True)  # e.g., "Phuket" or "Krabi"

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    duration_nights = Column(Integer, index=True)
    description = Column(String)
    is_recommended = Column(Boolean, default=False)
    days = relationship("ItineraryDay", back_populates="itinerary")

class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    day_number = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("locations.id"))
    
    itinerary = relationship("Itinerary", back_populates="days")
    hotel = relationship("Location")
    activities = relationship("Activity", back_populates="day")
    transfers = relationship("Transfer", back_populates="day")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    name = Column(String)
    description = Column(String)
    start_time = Column(String)  # Format: "HH:MM"
    duration_minutes = Column(Integer)
    
    day = relationship("ItineraryDay", back_populates="activities")
    location = relationship("Location")

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"))
    from_location_id = Column(Integer, ForeignKey("locations.id"))
    to_location_id = Column(Integer, ForeignKey("locations.id"))
    transport_type = Column(String)  # e.g., "car", "boat", "bus"
    departure_time = Column(String)  # Format: "HH:MM"
    duration_minutes = Column(Integer)
    
    day = relationship("ItineraryDay", back_populates="transfers")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id]) 