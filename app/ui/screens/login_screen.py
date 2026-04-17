from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.services.auth_service import AuthenticationService
from app.services.session_manager import SessionManager
from app.database.session import SessionLocal


class LoginScreen(QWidget):
    """Login screen for user authentication."""

    login_successful = Signal()

    def __init__(self, business_name: str = "Business Tool"):
        super().__init__()
        self.business_name = business_name
        self.auth_service = AuthenticationService()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Login - Business Tool")
        self.setFixedSize(400, 500)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Centered login panel
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        content_layout.setAlignment(Qt.AlignHCenter)
        content_widget.setFixedWidth(320)

        # Business name/logo at top
        title_label = QLabel(self.business_name)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        # Username field
        username_layout = QVBoxLayout()
        username_layout.setAlignment(Qt.AlignHCenter)
        username_label = QLabel("Username:")
        username_label.setFont(QFont("", 10, QFont.Weight.Bold))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        content_layout.addLayout(username_layout)

        # Password/PIN field
        password_layout = QVBoxLayout()
        password_layout.setAlignment(Qt.AlignHCenter)
        password_label = QLabel("Password or PIN:")
        password_label.setFont(QFont("", 10, QFont.Weight.Bold))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password or PIN")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        content_layout.addLayout(password_layout)

        # Show password checkbox
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        content_layout.addWidget(self.show_password_cb, alignment=Qt.AlignHCenter)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_button.setFont(QFont("", 12, QFont.Weight.Bold))
        self.login_button.clicked.connect(self.attempt_login)
        content_layout.addWidget(self.login_button)

        content_widget.setLayout(content_layout)

        horizontal_wrapper = QHBoxLayout()
        horizontal_wrapper.addStretch()
        horizontal_wrapper.addWidget(content_widget)
        horizontal_wrapper.addStretch()

        layout.addStretch()
        layout.addLayout(horizontal_wrapper)
        layout.addStretch()

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # Footer text
        footer_label = QLabel("Welcome to Business Tool")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: gray;")
        layout.addWidget(footer_label)

        self.setLayout(layout)

        # Set focus to username input
        self.username_input.setFocus()

        # Connect enter key to login
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.attempt_login)

    def toggle_password_visibility(self, state):
        """Toggle password field visibility."""
        if state == 2:  # Qt.CheckState.Checked.value is 2
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def attempt_login(self):
        """Attempt to authenticate the user."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self, "Login Error",
                "Please enter both username and password/PIN."
            )
            return

        try:
            user = self.auth_service.authenticate_user(username, password)
            if user:
                SessionManager.login_user(user)
                self.login_successful.emit()
                self.close()
            else:
                QMessageBox.warning(
                    self, "Login Failed",
                    "Invalid username or password/PIN."
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Login Error",
                f"An error occurred during login: {str(e)}"
            )

    def showEvent(self, event):
        """Clear fields when screen is shown."""
        super().showEvent(event)
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()