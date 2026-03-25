from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.stock_movement import StockMovement


class StockMovementRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, limit: int = 100) -> list[StockMovement]:
        stmt = (
            select(StockMovement)
            .order_by(StockMovement.created_at.desc(), StockMovement.id.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def create(self, **kwargs) -> StockMovement:
        movement = StockMovement(**kwargs)
        self.session.add(movement)
        self.session.flush()
        return movement
