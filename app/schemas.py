# schemas.py
# This file defines the Pydantic schemas for the IP Watcher application.
# These schemas are used for data validation and serialization.

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DeviceHistoryBase(BaseModel):
    is_online: bool
    timestamp: datetime

class DeviceHistory(DeviceHistoryBase):
    id: int

    class Config:
        orm_mode = True

class DeviceBase(BaseModel):
    ip_address: str
    mac_address: Optional[str] = None
    vendor: Optional[str] = None
    os_details: Optional[str] = None
    open_ports: Optional[str] = None
    is_online: bool = False
    name: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    first_seen: datetime
    last_seen: datetime
    history: List[DeviceHistory] = []

    class Config:
        orm_mode = True

class DeviceUpdate(BaseModel):
    name: str

class MQTTSettings(BaseModel):
    broker_url: str
    topic: str
    username: Optional[str] = None
    password: Optional[str] = None

class Config(BaseModel):
    ip_ranges: list[str]
    deep_scan_schedule: str
    ping_sweep_interval: int
    mqtt: MQTTSettings

class Version(BaseModel):
    version: str