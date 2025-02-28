from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
import sqlite3
from dashboard import DashboardWindow
from style import STYLE_SHEET  # Import the styles


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.resize(300, 250)

        # Username Field
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Enter Username")
        self.input_username.returnPressed.connect(self.focus_password)  # Move cursor to password on Enter

        # Password Field
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.returnPressed.connect(self.login)  # Login on Enter key

        # Buttons
        self.button_login = QPushButton("Login")
        self.button_register = QPushButton("Register")
        self.button_forgot_password = QPushButton("Forgot Password?")

        # Connect Buttons
        self.button_login.clicked.connect(self.login)
        self.button_register.clicked.connect(self.register)
        self.button_forgot_password.clicked.connect(self.reset_password)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)
        layout.addWidget(self.button_forgot_password)
        self.setLayout(layout)

    def focus_password(self):
        """Move cursor to the password field when Enter is pressed in the username field."""
        self.input_password.setFocus()

    def login(self):
        """Login the user after validating credentials."""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Success", "Login Successful!")
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password!")

    def register(self):
        """Register a new user."""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and Password cannot be empty!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            QMessageBox.warning(self, "Error", "Username already exists!")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", "Registration Successful!")
        conn.close()

    def reset_password(self):
        """Reset user password."""
        username = self.input_username.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Enter your username to reset password!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            new_password, ok = QMessageBox.getText(self, "Reset Password", "Enter your new password:")
            if ok and new_password:
                cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
                conn.commit()
                QMessageBox.information(self, "Success", "Password updated successfully!")
        else:
            QMessageBox.warning(self, "Error", "Username not found!")

        conn.close()


# Run the App
app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles
window = LoginWindow()
window.show()
app.exec()
