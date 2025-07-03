# api.py
# This file defines the API endpoints for the IP Watcher application.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

# Create a new API router.
api_router = APIRouter()

@api_router.get("/devices", response_model=list[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of devices from the database.
    """
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices

@api_router.get("/config", response_model=schemas.Config)
def read_config():
    """
    Retrieve the current application configuration.
    """
    return crud.get_config()

@api_router.post("/config", response_model=schemas.Config)
def update_config(config: schemas.Config):
    """
    Update the application configuration.
    """
    crud.update_config(config)
    return config
