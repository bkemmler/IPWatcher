
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.crud import get_device, get_devices, create_device, update_device_name
from app.database import Base
from app.models import Device
from app.schemas import DeviceCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crud.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_get_devices(db_session):
    devices = get_devices(db_session)
    assert len(devices) == 0

    db_device = Device(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01")
    db_session.add(db_device)
    db_session.commit()

    devices = get_devices(db_session)
    assert len(devices) == 1
    assert devices[0].ip_address == "1.1.1.1"


def test_get_device(db_session):
    db_device = Device(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01")
    db_session.add(db_device)
    db_session.commit()

    device = get_device(db_session, db_device.id)
    assert device.ip_address == "1.1.1.1"


def test_create_device(db_session):
    device_create = DeviceCreate(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01")
    device = create_device(db_session, device_create)
    assert device.ip_address == "1.1.1.1"

    db_device = db_session.query(Device).first()
    assert db_device.ip_address == "1.1.1.1"


def test_update_device_name(db_session):
    db_device = Device(ip_address="1.1.1.1", mac_address="00:00:00:00:00:01", name="old_name")
    db_session.add(db_device)
    db_session.commit()

    device = update_device_name(db_session, db_device.id, "new_name")
    assert device.name == "new_name"

    db_device = db_session.query(Device).filter(Device.id == db_device.id).first()
    assert db_device.name == "new_name"
