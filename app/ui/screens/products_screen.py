from PySide6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from app.database.session import SessionLocal
from app.database.models.product import Product


class ProductsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.title = QLabel("Products")
        self.refresh_btn = QPushButton("Refresh")
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Buying Price", "Selling Price", "Stock"])

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.table)

        self.refresh_btn.clicked.connect(self.load_products)
        self.load_products()

    def load_products(self) -> None:
        with SessionLocal() as session:
            products = session.query(Product).order_by(Product.id.desc()).all()

        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product.buying_price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{product.selling_price:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product.quantity_in_stock:.2f}"))