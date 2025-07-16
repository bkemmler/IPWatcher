# crud.py
# This file contains CRUD (Create, Read, Update, Delete) operations for the database.

from sqlalchemy.orm import Session
import yaml
from models import Device, DeviceHistory
from schemas import DeviceCreate, DeviceBase, Config
from config import settings
from datetime import datetime

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_device_by_mac(db: Session, mac_address: str):
    return db.query(models.Device).filter(models.Device.mac_address == mac_address).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, db_device: models.Device, device_update: schemas.DeviceBase):
    for key, value in device_update.dict(exclude_unset=True).items():
        setattr(db_device, key, value)
    db_device.last_seen = datetime.utcnow()
    db.commit()
    db.refresh(db_deivce)
    return db_device

def update_device_name(db: Session, device_id: int, name: str):
    db_device = get_device(db, device_id)
    if db_device:
        db_device.name = name
        db.commit()
        db.refresh(db_device)
    return db_device

def create_device_history(db: Session, device_id: int, is_online: bool):
    db_history = models.DeviceHistory(device_id=device_id, is_online=is_online)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_config():
    return settings

def update_config(config: schemas.Config):
    with open("/config/config.yaml", "w") as f:
        yaml.dump(config.dict(), f)
    settings.reload()