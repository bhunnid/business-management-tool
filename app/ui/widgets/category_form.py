from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from app.database.models.category import Category


class CategoryFormDialog(QDialog):
    def __init__(self, parent=None, category: Category | None = None) -> None:
        super().__init__(parent)
        self.category = category
        self.setWindowTitle("Add Category" if category is None else "Edit Category")
        self.setModal(True)
        self.resize(360, 120)

        self.name_input = QLineEdit()

        form = QFormLayout()
        form.addRow("Name", self.name_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        if self.category is not None:
            self.name_input.setText(self.category.name)

    def _validate_and_accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Category name is required.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {"name": self.name_input.text().strip()}
