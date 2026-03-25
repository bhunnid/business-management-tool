from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings"))
        layout.addWidget(QLabel("Later: business profile, backup, currency, tax"))
        layout.addStretch()