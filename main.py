import sys
from PyQt6.QtWidgets import QApplication
from login import LoginWindow
from style import STYLE_SHEET  # Import the styles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles
