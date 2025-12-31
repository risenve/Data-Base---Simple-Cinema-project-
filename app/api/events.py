from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # data to string
    response_data = db_event.__dict__.copy()
    response_data['date'] = str(db_event.date) if db_event.date else None
    return response_data


# READ ALL 
@router.get("/", response_model=List[schemas.EventResponse])
def read_events(
    skip: int = 0, 
    limit: int = 100,  
    db: Session = Depends(get_db)
):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    
    # conv data to string
    result = []
    for event in events:
        event_dict = event.__dict__.copy()
        event_dict['date'] = str(event.date) if event.date else None
        result.append(event_dict)
    
    return result


# READ ONE
@router.get("/{event_id}", response_model=schemas.EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    #conv data to string 
    event_dict = event.__dict__.copy()
    event_dict['date'] = str(event.date) if event.date else None
    return event_dict


# UPDATE
@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int, 
    event_update: schemas.EventCreate, 
    db: Session = Depends(get_db)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for field, value in event_update.dict().items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    
    # сonv date to striiing
    response_data = db_event.__dict__.copy()
    response_data['date'] = str(db_event.date) if db_event.date else None
    return response_data


# DELETE
@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    
    return {"message": "Event deleted"}