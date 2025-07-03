# models.py
# This file defines the database models for the IP Watcher application.

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Device(Base):
    """
    The Device model represents a device that has been discovered on the network.
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    mac_address = Column(String)
    vendor = Column(String)
    os = Column(String)
    open_ports = Column(String)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
