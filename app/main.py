from fastapi import FastAPI
from app.api import events, correspondents, reportages, queries

app = FastAPI(
    title="Reportage Management API",
    description="API for managing events, correspondents and reportages",
    version="1.0.0"
)

app.include_router(events.router)
app.include_router(correspondents.router)
app.include_router(reportages.router)
app.include_router(queries.router)  # add later 

@app.get("/")
def root():
    return {"message": "Reportage Management API is running"}