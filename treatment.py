from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TreatmentPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Treatments")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Treatment Management Section"))

        self.setLayout(layout)
