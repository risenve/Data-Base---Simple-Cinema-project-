from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/reportages", tags=["reportages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ReportageResponse)
def create_reportage(
    reportage: schemas.ReportageCreate, 
    db: Session = Depends(get_db)
):
    # check if event exists
    event = db.query(models.Event).filter(
        models.Event.id == reportage.event_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    #check if correspondent exists
    correspondent = db.query(models.Correspondent).filter(
        models.Correspondent.id == reportage.correspondent_id
    ).first()
    if not correspondent:
        raise HTTPException(status_code=404, detail="Correspondent not found")
    
    db_reportage = models.Reportage(**reportage.dict())
    db.add(db_reportage)
    db.commit()
    db.refresh(db_reportage)
    return db_reportage

# READ ALL 
@router.get("/", response_model=List[schemas.ReportageResponse])
def read_reportages(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    reportages = db.query(models.Reportage).offset(skip).limit(limit).all()
    return reportages

# READ ONE
@router.get("/{reportage_id}", response_model=schemas.ReportageResponse)
def read_reportage(reportage_id: int, db: Session = Depends(get_db)):
    reportage = db.query(models.Reportage).filter(
        models.Reportage.id == reportage_id
    ).first()
    if reportage is None:
        raise HTTPException(status_code=404, detail="Reportage not found")
    return reportage

# UPDATE
@router.put("/{reportage_id}", response_model=schemas.ReportageResponse)
def update_reportage(
    reportage_id: int, 
    reportage_update: schemas.ReportageCreate,
    db: Session = Depends(get_db)
):
    db_reportage = db.query(models.Reportage).filter(
        models.Reportage.id == reportage_id
    ).first()
    if db_reportage is None:
        raise HTTPException(status_code=404, detail="Reportage not found")
    
    # check if event exists when updating event_id
    if reportage_update.event_id != db_reportage.event_id:
        event = db.query(models.Event).filter(
            models.Event.id == reportage_update.event_id
        ).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
    
    if reportage_update.correspondent_id != db_reportage.correspondent_id:
        correspondent = db.query(models.Correspondent).filter(
            models.Correspondent.id == reportage_update.correspondent_id
        ).first()
        if not correspondent:
            raise HTTPException(status_code=404, detail="Correspondent not found")
    
    for field, value in reportage_update.dict().items():
        setattr(db_reportage, field, value)
    
    db.commit()
    db.refresh(db_reportage)
    return db_reportage

# DELETE
@router.delete("/{reportage_id}")
def delete_reportage(reportage_id: int, db: Session = Depends(get_db)):
    db_reportage = db.query(models.Reportage).filter(
        models.Reportage.id == reportage_id
    ).first()
    if db_reportage is None:
        raise HTTPException(status_code=404, detail="Reportage not found")
    
    db.delete(db_reportage)
    db.commit()
    return {"message": "Reportage deleted"}