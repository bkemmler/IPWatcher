# main.py
# Main application file for the IP Watcher.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import api_router
from .database import create_db_and_tables
from .scheduler import scheduler

# Create a FastAPI application instance.
app = FastAPI()

@app.on_event("startup")
def startup_event():
    """
    This function is called when the application starts.
    It creates the database and tables if they don't exist,
    and starts the background scheduler.
    """
    create_db_and_tables()
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    """
    This function is called when the application shuts down.
    It stops the background scheduler.
    """
    scheduler.shutdown()

# Include the API router, which handles all API endpoints.
app.include_router(api_router, prefix="/api")

# Mount the static files directory, which contains the frontend.
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/healthz")
def healthz():
    """
    A simple healthcheck endpoint that returns a 200 OK response.
    """
    return {"status": "ok"}
