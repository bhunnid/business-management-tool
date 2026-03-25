from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.expense import Expense


class ExpenseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, business_id: int, limit: int = 100) -> list[Expense]:
        stmt = (
            select(Expense)
            .where(Expense.business_id == business_id)
            .order_by(Expense.created_at.desc(), Expense.id.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def create(self, **kwargs) -> Expense:
        expense = Expense(**kwargs)
        self.session.add(expense)
        self.session.commit()
        self.session.refresh(expense)
        return expense
