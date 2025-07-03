# crud.py
# This file contains CRUD (Create, Read, Update, Delete) operations for the database.

from sqlalchemy.orm import Session
import yaml
from . import models, schemas
from .config import settings

def get_device(db: Session, device_id: int):
    """
    Retrieve a single device from the database by its ID.
    """
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_device_by_ip(db: Session, ip_address: str):
    """
    Retrieve a single device from the database by its IP address.
    """
    return db.query(models.Device).filter(models.Device.ip_address == ip_address).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of devices from the database.
    """
    return db.query(models.Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    """
    Create a new device in the database.
    """
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_config():
    """
    Retrieve the current application configuration.
    """
    return settings

def update_config(config: schemas.Config):
    """
    Update the application configuration.
    """
    with open("/config/config.yaml", "w") as f:
        yaml.dump(config.dict(), f)
    settings.reload()
