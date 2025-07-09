#!/usr/bin/env python

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Device

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_read_version():
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": "2.0.0"}


def test_read_devices(db_session):
    response = client.get("/api/devices")
    assert response.status_code == 200
    assert response.json() == []

    db_session.add(Device(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01"))
    db_session.commit()

    response = client.get("/api/devices")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ip_address"] == "1.1.1.1"


def test_update_device_name(db_session):
    device = Device(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01", name="old_name")
    db_session.add(device)
    db_session.commit()

    response = client.put(f"/api/devices/{device.id}", json={"name": "new_name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new_name"

    db_device = db_session.query(Device).filter(Device.id == device.id).first()
    assert db_device.name == "new_name"
