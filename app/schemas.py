from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any
import json

class EventCreate(BaseModel):
    place: str
    city: str
    date: str
    duration: int
    danger: str
    type: str
    extra_metadata: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if data.get('extra_metadata'):
            data['extra_metadata'] = json.dumps(data['extra_metadata'])
        return data

class EventResponse(BaseModel):
    id: int
    place: str
    city: str
    date: str
    duration: int
    danger: str
    type: str
    extra_metadata: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('extra_metadata', mode='before')
    @classmethod
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return None
        return v

class CorrespondentCreate(BaseModel):
    name: str
    country: str
    city: str
    specification: str
    operator: bool
    price: float
    
    model_config = ConfigDict(from_attributes=True)

class CorrespondentResponse(CorrespondentCreate):
    id: int

class ReportageCreate(BaseModel):
    date: str
    quality: str
    time: str 
    video: bool
    event_id: int
    correspondent_id: int
    
    model_config = ConfigDict(from_attributes=True)

class ReportageResponse(ReportageCreate):
    id: int