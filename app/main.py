from fastapi import FastAPI
from app.api.events import router as events_router
from app.api.correspondents import router as correspondents_router
from app.api.reportages import router as reportages_router
from app.api.queries import router as queries_router

app = FastAPI(
    title="Reportage Management API",
    description="API for managing events, correspondents and reportages",
    version="1.0.0"
)

app.include_router(events_router)
app.include_router(correspondents_router)
app.include_router(reportages_router)
app.include_router(queries_router)  

@app.get("/")
def root():
    return {"message": "Reportage Management API is running"}