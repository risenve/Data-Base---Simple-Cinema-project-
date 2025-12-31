from pydantic import BaseModel, ConfigDict
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
        # Конвертируем dict в JSON строку для SQLAlchemy
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
