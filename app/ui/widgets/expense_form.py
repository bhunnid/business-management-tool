from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from app.services.expense_service import ExpenseService


class ExpenseFormDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Record Expense")
        self.resize(420, 260)

        self.category_input = QComboBox()
        self.category_input.addItems(ExpenseService.DEFAULT_CATEGORIES)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000_000)
        self.amount_input.setDecimals(2)
        self.amount_input.setMinimum(0.01)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItems(["cash", "mpesa"])

        self.reference_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Optional note")

        form = QFormLayout()
        form.addRow("Category", self.category_input)
        form.addRow("Amount", self.amount_input)
        form.addRow("Payment", self.payment_method_input)
        form.addRow("M-Pesa Code / Ref", self.reference_input)
        form.addRow("Note", self.description_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _validate_and_accept(self) -> None:
        if self.amount_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than zero.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "category": self.category_input.currentText(),
            "amount": float(self.amount_input.value()),
            "payment_method": self.payment_method_input.currentText(),
            "reference": self.reference_input.text().strip() or None,
            "description": self.description_input.toPlainText().strip() or None,
        }
