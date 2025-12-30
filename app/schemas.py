from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import time

class EventCreate(BaseModel):
    place: str
    city: str
    date: str
    duration: int
    danger: str
    type: str
    extra_metadata: Optional[Dict[str, Any]] = None

class CorrespondentCreate(BaseModel):
    name: str
    country: str
    city: str
    specification: str
    operator: bool
    price: float

class ReportageCreate(BaseModel):
    date: str
    quality: str
    time: str 
    video: bool
    event_id: int
    correspondent_id: int

class EventResponse(EventCreate):
    id: int
    
    class Config:
        from_attributes = True

class CorrespondentResponse(CorrespondentCreate):
    id: int
    
    class Config:
        from_attributes = True

class ReportageResponse(ReportageCreate):
    id: int
    
    class Config:
        from_attributes = True