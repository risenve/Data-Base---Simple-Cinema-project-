from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    place: str
    city: str
    date: str
    duration: int
    danger: str
    type: str

class Correspondent(BaseModel):
    name: str
    country: str
    city: str
    specification: str
    operator: bool
    price: float

class Reportage(BaseModel):
    date: str
    quality: str
    time: str
    video: bool
    event_id: int
    correspondent_id: int