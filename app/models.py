# models.py
# This file defines the database models for the IP Watcher application.

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Device(Base):
    """
    The Device model represents a device that has been discovered on the network.
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ip_address = Column(String, index=True)
    mac_address = Column(String, unique=True, index=True)
    vendor = Column(String)
    os_details = Column(String)
    open_ports = Column(String)
    is_online = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    history = relationship("DeviceHistory", back_populates="device")


class DeviceHistory(Base):
    """
    The DeviceHistory model stores the online/offline history of a device.
    """
    __tablename__ = "device_history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    is_online = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="history")