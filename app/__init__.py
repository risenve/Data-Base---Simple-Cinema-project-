from fastapi import FastAPI
from app.api.events import router as events_router
from app.api.correspondents import router as correspondents_router
from app.api.reportages import router as reportages_router

__all__ = ["events_router", "correspondents_router", "reportages_router"]