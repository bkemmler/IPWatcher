# schemas.py
# This file defines the Pydantic schemas for the IP Watcher application.
# These schemas are used for data validation and serialization.

from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    """
    The base schema for a device.
    """
    ip_address: str
    mac_address: str | None = None
    vendor: str | None = None
    os: str | None = None
    open_ports: str | None = None

class DeviceCreate(DeviceBase):
    """
    The schema for creating a new device.
    """
    pass

class Device(DeviceBase):
    """
    The schema for a device that has been retrieved from the database.
    """
    id: int
    first_seen: datetime
    last_seen: datetime

    class Config:
        orm_mode = True

class MQTTSettings(BaseModel):
    """
    The schema for the MQTT settings.
    """
    broker_url: str
    topic: str
    username: str | None = None
    password: str | None = None

class Config(BaseModel):
    """
    The schema for the application configuration.
    """
    ip_ranges: list[str]
    deep_scan_schedule: str
    ping_sweep_interval: int
    mqtt: MQTTSettings
