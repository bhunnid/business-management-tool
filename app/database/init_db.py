import logging
import sys
from pathlib import Path

from sqlalchemy import inspect

from app.core.config import DATABASE_URL, DATA_DIR
from app.database.base import Base
from app.database import models  # noqa: F401
from app.database.session import engine

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize the database by:
    1. Ensuring the data directory exists
    2. Creating all tables from SQLAlchemy models
    3. Verifying all required tables are present
    """
    # Ensure data directory exists
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Data directory ready: {DATA_DIR}")
    except Exception as e:
        logger.exception(f"Failed to create data directory: {e}")
        raise

    # Create all tables from SQLAlchemy models
    try:
        logger.info("Creating database tables from models...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.exception(f"Failed to create database tables: {e}")
        raise

    # Verify that at least the businesses table exists
    try:
        with engine.begin() as conn:
            inspector = inspect(conn)
            existing_tables = set(inspector.get_table_names())
        
        logger.info(f"Existing tables: {existing_tables}")
        
        # Check for critical table
        if "businesses" not in existing_tables:
            logger.error("CRITICAL: 'businesses' table was not created!")
            raise RuntimeError(
                "Database initialization failed: 'businesses' table does not exist. "
                "Please ensure write permissions to the data directory."
            )
        
        logger.info("Database initialization complete - all required tables present")
        
    except Exception as e:
        logger.exception(f"Failed to verify database tables: {e}")
        raise