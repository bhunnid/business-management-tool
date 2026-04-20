import logging
from sqlalchemy import select

from app.database.models.business import Business
from app.database.session import SessionLocal

logger = logging.getLogger(__name__)


def ensure_default_business() -> Business:
    """
    Ensure at least one business exists in the database.
    This should only be called AFTER init_db() has completed successfully.
    """
    try:
        with SessionLocal() as session:
            # Check if any business already exists
            existing = session.scalar(select(Business).limit(1))
            if existing:
                logger.info(f"Default business already exists: {existing.business_name}")
                return existing

            # Create a new default business
            logger.info("Creating default business...")
            business = Business(
                business_name="My Business",
                business_type="Retail Shop",
                phone="",
                location="",
            )
            session.add(business)
            session.commit()
            session.refresh(business)
            logger.info(f"Default business created successfully with ID: {business.id}")
            return business
    except Exception as e:
        logger.exception(f"Failed to ensure default business exists: {e}")
        raise RuntimeError(
            f"Failed to create default business in database. "
            f"This typically indicates a database permission or configuration issue. "
            f"Error: {str(e)}"
        )


