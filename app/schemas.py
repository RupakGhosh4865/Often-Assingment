from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class LocationType(str, Enum):
    CITY = "city"
    ATTRACTION = "attraction"
    HOTEL = "hotel"

class LocationBase(BaseModel):
    name: str
    type: LocationType
    description: str
    latitude: float
    longitude: float
    region: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    description: str
    start_time: str
    duration_minutes: int
    location_id: int

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True

class TransferBase(BaseModel):
    from_location_id: int
    to_location_id: int
    transport_type: str
    departure_time: str
    duration_minutes: int

class TransferCreate(TransferBase):
    pass

class Transfer(TransferBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True

class ItineraryDayBase(BaseModel):
    day_number: int
    hotel_id: int

class ItineraryDayCreate(ItineraryDayBase):
    activities: List[ActivityCreate]
    transfers: List[TransferCreate]

class ItineraryDay(ItineraryDayBase):
    id: int
    itinerary_id: int
    activities: List[Activity]
    transfers: List[Transfer]

    class Config:
        from_attributes = True

class ItineraryBase(BaseModel):
    name: str
    duration_nights: int
    description: str
    is_recommended: bool = False

class ItineraryCreate(ItineraryBase):
    days: List[ItineraryDayCreate]

class Itinerary(ItineraryBase):
    id: int
    days: List[ItineraryDay]

    class Config:
        from_attributes = True

class ItineraryRecommendation(BaseModel):
    duration_nights: int 