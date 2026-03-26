from PySide6.QtCore import Qt
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
from app.services.category_service import CategoryService
from app.ui.widgets.category_form import CategoryFormDialog


class CategoriesScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.business = ensure_default_business()
        self.category_service = CategoryService()
        self.categories = []

        self.title = QLabel("Categories")
        self.title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.add_btn = QPushButton("Add Category")
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setEnabled(False)
        self.delete_btn = QPushButton("Remove")
        self.delete_btn.setEnabled(False)
        self.refresh_btn = QPushButton("Refresh")

        actions = QHBoxLayout()
        actions.addWidget(self.add_btn)
        actions.addWidget(self.edit_btn)
        actions.addWidget(self.delete_btn)
        actions.addStretch()
        actions.addWidget(self.refresh_btn)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.empty_state_label = QLabel("No categories yet. Add one to get started.")
        self.empty_state_label.setStyleSheet("color: #999; font-size: 13px; text-align: center;")
        self.empty_state_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addLayout(actions)
        layout.addWidget(self.empty_state_label)
        layout.addWidget(self.table)

        self.add_btn.clicked.connect(self.add_category)
        self.edit_btn.clicked.connect(self.edit_selected_category)
        self.delete_btn.clicked.connect(self.delete_selected_category)
        self.refresh_btn.clicked.connect(self.load_categories)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        self.load_categories()

    def on_selection_changed(self) -> None:
        """Enable/disable buttons based on selection."""
        has_selection = self.table.currentRow() >= 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def load_categories(self) -> None:
        self.categories = self.category_service.list_categories(self.business.id)
        self.table.setRowCount(len(self.categories))

        # Show/hide empty state
        if len(self.categories) == 0:
            self.empty_state_label.setVisible(True)
            self.table.setVisible(False)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        else:
            self.empty_state_label.setVisible(False)
            self.table.setVisible(True)

        for row, category in enumerate(self.categories):
            self.table.setItem(row, 0, QTableWidgetItem(str(category.id)))
            self.table.setItem(row, 1, QTableWidgetItem(category.name))

        self.table.resizeColumnsToContents()

    def get_selected_category(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        category_id_item = self.table.item(row, 0)
        if category_id_item is None:
            return None

        category_id = int(category_id_item.text())
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def add_category(self) -> None:
        dialog = CategoryFormDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.category_service.create_category(self.business.id, data["name"])
                QMessageBox.information(self, "Success", "Category added successfully.")
                self.load_categories()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def edit_selected_category(self) -> None:
        category = self.get_selected_category()
        if category is None:
            QMessageBox.information(self, "No Selection", "Select a category first.")
            return

        dialog = CategoryFormDialog(self, category=category)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.category_service.update_category(category.id, self.business.id, data["name"])
                QMessageBox.information(self, "Success", "Category updated successfully.")
                self.load_categories()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def delete_selected_category(self) -> None:
        category = self.get_selected_category()
        if category is None:
            QMessageBox.information(self, "No Selection", "Select a category first.")
            return

        result = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete category '{category.name}'?",
        )
        if result != QMessageBox.Yes:
            return

        try:
            self.category_service.delete_category(category.id)
            QMessageBox.information(self, "Success", "Category removed successfully.")
            self.load_categories()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
