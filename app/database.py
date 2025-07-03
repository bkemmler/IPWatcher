# database.py
# This file contains the database configuration and session management.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL.
# This uses a SQLite database stored in the /data directory.
SQLALCHEMY_DATABASE_URL = "sqlite:////data/ip_watcher.db"

# Create a new SQLAlchemy engine.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a new SQLAlchemy session factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new SQLAlchemy base class.
Base = declarative_base()

def create_db_and_tables():
    """
    Create the database and tables if they don't already exist.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    A dependency that provides a database session to the API endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
