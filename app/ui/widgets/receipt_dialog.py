from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ReceiptDialog(QDialog):
    """Dialog for displaying receipts in a readable format."""

    def __init__(self, receipt_data: dict, parent=None) -> None:
        super().__init__(parent)
        self.receipt_data = receipt_data

        self.setWindowTitle("Receipt")
        self.setGeometry(100, 100, 500, 700)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Business header
        business_name = QLabel(self.receipt_data.get("business_name", ""))
        business_name.setStyleSheet("font-size: 16px; font-weight: bold; text-align: center;")
        business_name.setAlignment(Qt.AlignCenter)

        business_info = []
        if self.receipt_data.get("location"):
            business_info.append(self.receipt_data["location"])
        if self.receipt_data.get("phone"):
            business_info.append(self.receipt_data["phone"])

        business_details = QLabel("\n".join(business_info))
        business_details.setStyleSheet("font-size: 9px; text-align: center; color: #555;")
        business_details.setAlignment(Qt.AlignCenter)

        # Receipt number and date/time
        receipt_header = QLabel(
            f"{self.receipt_data.get('sale_number', '')}\n"
            f"{self.receipt_data.get('date', '')} {self.receipt_data.get('time', '')}"
        )
        receipt_header.setStyleSheet("font-size: 10px; text-align: center; color: #555;")
        receipt_header.setAlignment(Qt.AlignCenter)

        # Separator
        separator = QLabel("-" * 50)
        separator.setStyleSheet("font-size: 10px; text-align: center; color: #999;")

        # Items table
        items_label = QLabel("Items")
        items_label.setStyleSheet("font-size: 11px; font-weight: bold;")

        items_table = QTableWidget(len(self.receipt_data.get("items", [])), 4)
        items_table.setHorizontalHeaderLabels(["Product", "Qty", "Price", "Total"])
        items_table.setStyleSheet("border: none; font-size: 10px;")
        items_table.horizontalHeader().setStretchLastSection(False)
        items_table.setColumnWidth(0, 150)
        items_table.setColumnWidth(1, 50)
        items_table.setColumnWidth(2, 70)
        items_table.setColumnWidth(3, 70)
        items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        items_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for row, item in enumerate(self.receipt_data.get("items", [])):
            product_item = QTableWidgetItem(item["product_name"])
            qty_item = QTableWidgetItem(f"{item['quantity']:.2f}")
            qty_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            price_item = QTableWidgetItem(f"{item['unit_price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item = QTableWidgetItem(f"{item['line_total']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            items_table.setItem(row, 0, product_item)
            items_table.setItem(row, 1, qty_item)
            items_table.setItem(row, 2, price_item)
            items_table.setItem(row, 3, total_item)

        items_table.setMaximumHeight(200)

        # Totals section
        separator2 = QLabel("-" * 50)
        separator2.setStyleSheet("font-size: 10px; text-align: center; color: #999;")

        totals_layout = QVBoxLayout()

        subtotal = self.receipt_data.get("subtotal", 0.0)
        subtotal_label = QLabel(f"Subtotal: {self.receipt_data.get('currency', 'KES')} {subtotal:.2f}")
        subtotal_label.setStyleSheet("font-size: 10px;")
        totals_layout.addWidget(subtotal_label)

        discount = self.receipt_data.get("discount", 0.0)
        if discount > 0:
            discount_label = QLabel(f"Discount: - {self.receipt_data.get('currency', 'KES')} {discount:.2f}")
            discount_label.setStyleSheet("font-size: 10px; color: #d9534f;")
            totals_layout.addWidget(discount_label)

        tax_amount = self.receipt_data.get("tax_amount", 0.0)
        tax_percent = self.receipt_data.get("tax_percent", 0.0)
        if tax_amount > 0:
            tax_label = QLabel(
                f"Tax ({tax_percent:.1f}%): {self.receipt_data.get('currency', 'KES')} {tax_amount:.2f}"
            )
            tax_label.setStyleSheet("font-size: 10px; color: #555;")
            totals_layout.addWidget(tax_label)

        total = self.receipt_data.get("total", 0.0)
        total_label = QLabel(f"Total: {self.receipt_data.get('currency', 'KES')} {total:.2f}")
        total_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        totals_layout.addWidget(total_label)

        # Payment method
        payment_label = QLabel(f"Payment: {self.receipt_data.get('payment_method', '')}")
        payment_label.setStyleSheet("font-size: 10px; color: #555;")
        totals_layout.addWidget(payment_label)

        # Footer text
        separator3 = QLabel("-" * 50)
        separator3.setStyleSheet("font-size: 10px; text-align: center; color: #999;")
        totals_layout.addWidget(separator3)

        footer_text = self.receipt_data.get("footer_text", "")
        if footer_text:
            footer_label = QLabel(footer_text)
            footer_label.setStyleSheet("font-size: 9px; text-align: center; color: #666;")
            footer_label.setAlignment(Qt.AlignCenter)
            footer_label.setWordWrap(True)
            totals_layout.addWidget(footer_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)

        # Main layout
        layout.addWidget(business_name)
        layout.addWidget(business_details)
        layout.addWidget(receipt_header)
        layout.addWidget(separator)
        layout.addWidget(items_label)
        layout.addWidget(items_table)
        layout.addWidget(separator2)
        layout.addLayout(totals_layout)
        layout.addLayout(buttons_layout)
