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

# CREATE (проверяем существование event и correspondent)
@router.post("/", response_model=schemas.ReportageResponse)
def create_reportage(
    reportage: schemas.ReportageCreate, 
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли event
    event = db.query(models.Event).filter(
        models.Event.id == reportage.event_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Проверяем, существует ли correspondent
    correspondent = db.query(models.Correspondent).filter(
        models.Correspondent.id == reportage.correspondent_id
    ).first()
    if not correspondent:
        raise HTTPException(status_code=404, detail="Correspondent not found")
    
    db_reportage = models.Reportage(**reportage.dict())
    db.add(db_reportage)
    db.commit()
    db.refresh(db_reportage)
    
    # Конвертируем дату и время в строки для ответа
    return {
        "id": db_reportage.id,
        "date": str(db_reportage.date) if db_reportage.date else None,
        "quality": db_reportage.quality,
        "time": str(db_reportage.time) if db_reportage.time else None,
        "video": db_reportage.video,
        "event_id": db_reportage.event_id,
        "correspondent_id": db_reportage.correspondent_id
    }

# READ ALL (с пагинацией)
@router.get("/", response_model=List[schemas.ReportageResponse])
def read_reportages(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    reportages = db.query(models.Reportage).offset(skip).limit(limit).all()
    
    # Конвертируем даты и время в строки
    result = []
    for reportage in reportages:
        result.append({
            "id": reportage.id,
            "date": str(reportage.date) if reportage.date else None,
            "quality": reportage.quality,
            "time": str(reportage.time) if reportage.time else None,
            "video": reportage.video,
            "event_id": reportage.event_id,
            "correspondent_id": reportage.correspondent_id
        })
    
    return result

# READ ONE
@router.get("/{reportage_id}", response_model=schemas.ReportageResponse)
def read_reportage(reportage_id: int, db: Session = Depends(get_db)):
    reportage = db.query(models.Reportage).filter(
        models.Reportage.id == reportage_id
    ).first()
    if reportage is None:
        raise HTTPException(status_code=404, detail="Reportage not found")
    
    return {
        "id": reportage.id,
        "date": str(reportage.date) if reportage.date else None,
        "quality": reportage.quality,
        "time": str(reportage.time) if reportage.time else None,
        "video": reportage.video,
        "event_id": reportage.event_id,
        "correspondent_id": reportage.correspondent_id
    }

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
    
    # Проверяем новые связи, если они изменились
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
    
    return {
        "id": db_reportage.id,
        "date": str(db_reportage.date) if db_reportage.date else None,
        "quality": db_reportage.quality,
        "time": str(db_reportage.time) if db_reportage.time else None,
        "video": db_reportage.video,
        "event_id": db_reportage.event_id,
        "correspondent_id": db_reportage.correspondent_id
    }

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