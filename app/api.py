# api.py
# This file defines the API endpoints for the IP Watcher application.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_config, update_config
from schemas import Config, Version, Device, DeviceUpdate
from scanner import scan_network
from database import get_db
from config import settings

# Create a new API router.
api_router = APIRouter()

@api_router.get("/version", response_model=schemas.Version)
def read_version():
    """
    Retrieve the application version.
    """
    return {"version": "3.0.0"}

@api_router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@api_router.get("/devices", response_model=list[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of devices from the database.
    """
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices

@api_router.put("/devices/{device_id}", response_model=schemas.Device)
def update_device_name(
    device_id: int, device_update: schemas.DeviceUpdate, db: Session = Depends(get_db)
):
    """
    Update the name of a device.
    """
    db_device = crud.update_device_name(db, device_id, device_update.name)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@api_router.post("/scan")
def trigger_scan():
    """
    Trigger a new network scan.
    """
    scanner.scan_network(settings.ip_ranges)
    return {"message": "Scan triggered"}

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