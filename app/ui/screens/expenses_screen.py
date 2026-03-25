from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database.seed import ensure_default_business
from app.services.expense_service import ExpenseService
from app.ui.widgets.expense_form import ExpenseFormDialog


class ExpensesScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.business = ensure_default_business()
        self.expense_service = ExpenseService()
        self.expenses = []

        self.title = QLabel("Expenses")
        self.title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.add_btn = QPushButton("Record Expense")
        self.refresh_btn = QPushButton("Refresh")

        actions = QHBoxLayout()
        actions.addWidget(self.add_btn)
        actions.addStretch()
        actions.addWidget(self.refresh_btn)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Category", "Amount", "Payment", "Reference", "Date"]
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addLayout(actions)
        layout.addWidget(self.table)

        self.add_btn.clicked.connect(self.add_expense)
        self.refresh_btn.clicked.connect(self.load_expenses)

        self.load_expenses()

    def load_expenses(self) -> None:
        self.expenses = self.expense_service.list_recent_expenses(self.business.id, limit=200)
        self.table.setRowCount(len(self.expenses))

        for row, expense in enumerate(self.expenses):
            self.table.setItem(row, 0, QTableWidgetItem(str(expense.id)))
            self.table.setItem(row, 1, QTableWidgetItem(expense.category))
            self.table.setItem(row, 2, QTableWidgetItem(f"{expense.amount:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(expense.payment_method.upper()))
            self.table.setItem(row, 4, QTableWidgetItem(expense.reference or ""))
            self.table.setItem(row, 5, QTableWidgetItem(expense.created_at.strftime("%Y-%m-%d %H:%M")))

        self.table.resizeColumnsToContents()

    def add_expense(self) -> None:
        dialog = ExpenseFormDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.expense_service.create_expense(
                    business_id=self.business.id,
                    category=data["category"],
                    amount=data["amount"],
                    description=data["description"],
                    payment_method=data["payment_method"],
                    reference=data["reference"],
                    recorded_by=None,
                )
                self.load_expenses()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))
