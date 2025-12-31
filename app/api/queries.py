from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/queries", tags=["queries"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. SELECT ... WHERE 
@router.get("/events_by_city_and_danger")
def get_events_by_city_and_danger(
    city: str = Query(..., description="City name"),
    danger_level: str = Query(..., description="Danger level (low/medium/high)"),
    min_duration: Optional[int] = Query(None, description="Minimum duration in minutes"),
    db: Session = Depends(get_db)
):
    """SELECT events WHERE city = ? AND danger = ? AND duration >= ?"""
    query = db.query(models.Event).filter(
        models.Event.city == city,
        models.Event.danger == danger_level
    )
    
    if min_duration:
        query = query.filter(models.Event.duration >= min_duration)
    
    return query.all()


# 2. JOIN 
@router.get("/reportages_with_details")
def get_reportages_with_details(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """JOIN reportages with events and correspondents"""
    results = db.query(
        models.Reportage,
        models.Event,
        models.Correspondent
    ).join(
        models.Event, models.Reportage.event_id == models.Event.id
    ).join(
        models.Correspondent, models.Reportage.correspondent_id == models.Correspondent.id
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "reportage_id": r.id,
            "reportage_date": r.date,
            "quality": r.quality,
            "event_title": e.place if e else None,
            "event_city": e.city if e else None,
            "correspondent_name": c.name if c else None,
            "correspondent_spec": c.specification if c else None
        }
        for r, e, c in results
    ]


# 3. UPDATE 
@router.put("/increase_operator_prices")
def increase_operator_prices(
    percentage: float = Query(10.0, ge=0.0, le=100.0, description="Percentage increase"),
    min_price: Optional[float] = Query(100.0, description="Minimum current price to update"),
    db: Session = Depends(get_db)
):
    """UPDATE correspondent SET price = price * (1 + ?/100) WHERE operator = TRUE AND price >= ?"""
    multiplier = 1 + (percentage / 100.0)
    
    query = db.query(models.Correspondent).filter(
        models.Correspondent.operator == True
    )
    
    if min_price:
        query = query.filter(models.Correspondent.price >= min_price)
    
    correspondents = query.all()
    updated_count = 0
    
    for corr in correspondents:
        corr.price = round(corr.price * multiplier, 2)
        updated_count += 1
    
    db.commit()
    
    return {
        "message": f"Updated {updated_count} correspondents",
        "percentage_increase": percentage,
        "multiplier": multiplier
    }


# 4. GROUP BY 
@router.get("/events_stats_by_city")
def get_events_stats_by_city(db: Session = Depends(get_db)):
    """GROUP BY city with aggregate functions"""
    stats = db.query(
        models.Event.city,
        func.count(models.Event.id).label("total_events"),
        func.avg(models.Event.duration).label("avg_duration"),
        func.min(models.Event.duration).label("min_duration"),
        func.max(models.Event.duration).label("max_duration")
    ).group_by(models.Event.city).all()
    
    return [
        {
            "city": city,
            "total_events": total_events,
            "avg_duration": float(avg_duration) if avg_duration else 0,
            "min_duration": min_duration,
            "max_duration": max_duration
        }
        for city, total_events, avg_duration, min_duration, max_duration in stats
    ]


# 5. SORT 
@router.get("/sorted_events")
def get_sorted_events(
    sort_by: str = Query("date", description="Field to sort by (date, duration, city)"),
    order: str = Query("desc", description="Sort order (asc or desc)"),
    limit: int = Query(50, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """SORT events by specified field and order"""
    
    sort_field = None
    if sort_by == "date":
        sort_field = models.Event.date
    elif sort_by == "duration":
        sort_field = models.Event.duration
    elif sort_by == "city":
        sort_field = models.Event.city
    else:
        sort_field = models.Event.date  # default
    
    if order.lower() == "asc":
        query = db.query(models.Event).order_by(sort_field.asc())
    else:
        query = db.query(models.Event).order_by(sort_field.desc())
    
    return query.limit(limit).all()


@router.get("/search_events_json")
def search_events_json(
    q: str = Query(..., description="Regex pattern to search in extra_metadata"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Full-text search in extra_metadata JSON field using regex"""
    from sqlalchemy import text
    
    results = db.query(models.Event).filter(
        models.Event.extra_metadata.cast(text).op("~*")(q)
    ).limit(limit).all()
    
    return results
