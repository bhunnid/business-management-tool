from sqlalchemy import select

from app.database.models.business import Business
from app.database.session import SessionLocal


class SettingsService:
    """Service for managing business settings and preferences."""

    def get_business_settings(self, business_id: int) -> Business | None:
        """Retrieve business settings by business ID."""
        with SessionLocal() as session:
            business = session.scalar(
                select(Business).where(Business.id == business_id)
            )
            if business:
                # Detach from session before returning
                session.expunge(business)
            return business

    def update_business_settings(
        self,
        business_id: int,
        business_name: str | None = None,
        phone: str | None = None,
        location: str | None = None,
        currency: str | None = None,
        tax_percent: float | None = None,
        receipt_footer: str | None = None,
    ) -> Business | None:
        """Update business settings."""
        with SessionLocal() as session:
            business = session.scalar(
                select(Business).where(Business.id == business_id)
            )
            if not business:
                return None

            if business_name is not None:
                business.business_name = business_name.strip()
            if phone is not None:
                business.phone = phone.strip() if phone else None
            if location is not None:
                business.location = location.strip() if location else None
            if currency is not None:
                business.currency = currency.strip() if currency else "KES"
            if tax_percent is not None:
                business.tax_percent = float(tax_percent) if tax_percent else 0.0
            if receipt_footer is not None:
                business.receipt_footer = receipt_footer.strip() if receipt_footer else None

            session.commit()
            session.refresh(business)
            session.expunge(business)
            return business
