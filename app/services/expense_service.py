from app.database.models.expense import Expense
from app.database.repositories.expense_repo import ExpenseRepository
from app.database.session import SessionLocal


class ExpenseService:
    DEFAULT_CATEGORIES = [
        "Rent",
        "Salaries",
        "Transport",
        "Utilities",
        "Stock Purchase",
        "Miscellaneous",
    ]

    ALLOWED_PAYMENT_METHODS = {"cash", "mpesa"}

    def list_recent_expenses(self, business_id: int, limit: int = 100) -> list[Expense]:
        with SessionLocal() as session:
            repo = ExpenseRepository(session)
            return repo.list_recent(business_id, limit=limit)

    def create_expense(
        self,
        business_id: int,
        category: str,
        amount: float,
        description: str | None = None,
        payment_method: str = "cash",
        reference: str | None = None,
        recorded_by: int | None = None,
    ) -> Expense:
        category = category.strip()
        if not category:
            raise ValueError("Expense category is required.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        payment_method = payment_method.strip().lower()
        if payment_method not in self.ALLOWED_PAYMENT_METHODS:
            raise ValueError("Invalid payment method.")

        with SessionLocal() as session:
            repo = ExpenseRepository(session)
            return repo.create(
                business_id=business_id,
                category=category,
                amount=amount,
                description=(description or "").strip() or None,
                payment_method=payment_method,
                reference=(reference or "").strip() or None,
                recorded_by=recorded_by,
            )
