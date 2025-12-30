from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/correspondents", tags=["correspondents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", response_model=schemas.CorrespondentResponse)
def create_correspondent(
    correspondent: schemas.CorrespondentCreate, 
    db: Session = Depends(get_db)
):
    db_correspondent = models.Correspondent(**correspondent.dict())
    db.add(db_correspondent)
    db.commit()
    db.refresh(db_correspondent)
    return db_correspondent

# READ ALL 
@router.get("/", response_model=List[schemas.CorrespondentResponse])
def read_correspondents(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    correspondents = db.query(models.Correspondent).offset(skip).limit(limit).all()
    return correspondents

# READ ONE
@router.get("/{correspondent_id}", response_model=schemas.CorrespondentResponse)
def read_correspondent(correspondent_id: int, db: Session = Depends(get_db)):
    correspondent = db.query(models.Correspondent).filter(
        models.Correspondent.id == correspondent_id
    ).first()
    if correspondent is None:
        raise HTTPException(status_code=404, detail="Correspondent not found")
    return correspondent

# UPDATE
@router.put("/{correspondent_id}", response_model=schemas.CorrespondentResponse)
def update_correspondent(
    correspondent_id: int, 
    correspondent_update: schemas.CorrespondentCreate,
    db: Session = Depends(get_db)
):
    db_correspondent = db.query(models.Correspondent).filter(
        models.Correspondent.id == correspondent_id
    ).first()
    if db_correspondent is None:
        raise HTTPException(status_code=404, detail="Correspondent not found")
    
    for field, value in correspondent_update.dict().items():
        setattr(db_correspondent, field, value)
    
    db.commit()
    db.refresh(db_correspondent)
    return db_correspondent

# DELETE
@router.delete("/{correspondent_id}")
def delete_correspondent(correspondent_id: int, db: Session = Depends(get_db)):
    db_correspondent = db.query(models.Correspondent).filter(
        models.Correspondent.id == correspondent_id
    ).first()
    if db_correspondent is None:
        raise HTTPException(status_code=404, detail="Correspondent not found")
    
    db.delete(db_correspondent)
    db.commit()
    return {"message": "Correspondent deleted"}