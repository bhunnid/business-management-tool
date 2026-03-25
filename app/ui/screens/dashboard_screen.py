from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Dashboard"))
        layout.addWidget(QLabel("Later: sales summary, low stock alerts, KPIs"))
        layout.addStretch()