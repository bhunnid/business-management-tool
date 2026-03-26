from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
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
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.services.signals import app_signals
from app.ui.widgets.product_form import ProductFormDialog
from app.ui.widgets.stock_adjustment_dialog import StockAdjustmentDialog


class ProductsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.product_service = ProductService()
        self.category_service = CategoryService()
        self.inventory_service = InventoryService()
        self.business = ensure_default_business()
        self.products = []

        self.title = QLabel("Products")
        self.title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.add_btn = QPushButton("Add Product")
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setEnabled(False)
        self.delete_btn = QPushButton("Remove")
        self.delete_btn.setEnabled(False)
        self.adjust_btn = QPushButton("Change Stock")
        self.adjust_btn.setEnabled(False)
        self.refresh_btn = QPushButton("Refresh")

        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.add_btn)
        actions_layout.addWidget(self.edit_btn)
        actions_layout.addWidget(self.delete_btn)
        actions_layout.addWidget(self.adjust_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.refresh_btn)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "SKU", "Buying Price", "Selling Price", "Stock"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.empty_state_label = QLabel("No products yet. Add one to get started.")
        self.empty_state_label.setStyleSheet("color: #999; font-size: 13px; text-align: center;")
        self.empty_state_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addLayout(actions_layout)
        layout.addWidget(self.empty_state_label)
        layout.addWidget(self.table)

        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_selected_product)
        self.delete_btn.clicked.connect(self.delete_selected_product)
        self.adjust_btn.clicked.connect(self.adjust_selected_stock)
        self.refresh_btn.clicked.connect(self.load_products)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        self.load_products()

    def on_selection_changed(self) -> None:
        """Enable/disable buttons based on selection."""
        has_selection = self.table.currentRow() >= 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.adjust_btn.setEnabled(has_selection)

    def load_products(self) -> None:
        self.products = self.product_service.list_products()
        self.table.setRowCount(len(self.products))

        # Show/hide empty state
        if len(self.products) == 0:
            self.empty_state_label.setVisible(True)
            self.table.setVisible(False)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.adjust_btn.setEnabled(False)
        else:
            self.empty_state_label.setVisible(False)
            self.table.setVisible(True)

        for row, product in enumerate(self.products):
            category_name = ""
            if getattr(product, "category", None) is not None:
                category_name = product.category.name

            items = [
                QTableWidgetItem(str(product.id)),
                QTableWidgetItem(product.name),
                QTableWidgetItem(category_name),
                QTableWidgetItem(product.sku or ""),
                QTableWidgetItem(f"{product.buying_price:.2f}"),
                QTableWidgetItem(f"{product.selling_price:.2f}"),
                QTableWidgetItem(f"{product.quantity_in_stock:.2f}"),
            ]

            for col, item in enumerate(items):
                if product.quantity_in_stock <= product.reorder_level:
                    item.setBackground(QColor(255, 230, 230))
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

    def get_selected_product(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        product_id = int(item.text())
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_product(self) -> None:
        categories = self.category_service.list_categories(self.business.id)
        dialog = ProductFormDialog(self, categories=categories)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.product_service.create_product(
                    business_id=self.business.id,
                    name=data["name"],
                    sku=data["sku"],
                    barcode=data["barcode"],
                    category_id=data["category_id"],
                    buying_price=data["buying_price"],
                    selling_price=data["selling_price"],
                    quantity_in_stock=data["quantity_in_stock"],
                    reorder_level=data["reorder_level"],
                )
                QMessageBox.information(self, "Success", "Product added successfully.")
                self.load_products()
                app_signals.product_changed.emit()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def edit_selected_product(self) -> None:
        product = self.get_selected_product()
        if product is None:
            QMessageBox.information(self, "No Selection", "Select a product first.")
            return

        categories = self.category_service.list_categories(self.business.id)
        dialog = ProductFormDialog(self, product=product, categories=categories)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.product_service.update_product(
                    product_id=product.id,
                    name=data["name"],
                    sku=data["sku"],
                    barcode=data["barcode"],
                    category_id=data["category_id"],
                    buying_price=data["buying_price"],
                    selling_price=data["selling_price"],
                    quantity_in_stock=data["quantity_in_stock"],
                    reorder_level=data["reorder_level"],
                )
                QMessageBox.information(self, "Success", "Product updated successfully.")
                self.load_products()
                app_signals.product_changed.emit()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def delete_selected_product(self) -> None:
        product = self.get_selected_product()
        if product is None:
            QMessageBox.information(self, "No Selection", "Select a product first.")
            return

        result = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete product '{product.name}'?",
        )
        if result != QMessageBox.Yes:
            return

        try:
            self.product_service.delete_product(product.id)
            QMessageBox.information(self, "Success", "Product removed successfully.")
            self.load_products()
            app_signals.product_changed.emit()
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def adjust_selected_stock(self) -> None:
        product = self.get_selected_product()
        if product is None:
            QMessageBox.information(self, "No Selection", "Select a product first.")
            return

        dialog = StockAdjustmentDialog(self, product=product)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.inventory_service.adjust_stock(
                    product_id=product.id,
                    movement_type=data["movement_type"],
                    quantity=data["quantity"],
                    reference=data["reference"],
                )
                QMessageBox.information(self, "Success", "Stock updated successfully.")
                self.load_products()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))
