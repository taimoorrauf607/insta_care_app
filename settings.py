from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings & Compliance Section"))

        self.setLayout(layout)
