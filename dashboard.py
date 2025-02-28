from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget,
    QApplication, QFrame
)
from appointments import AppointmentsPage
from clients import ClientPage
from billing import BillingPage
from treatment import TreatmentPage
from inventory import InventoryPage
from staff import StaffPage
from reports import ReportsPage
from settings import SettingsPage
from style import STYLE_SHEET  # Import global styles

# Initialize Application
app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRM Dashboard")
        self.resize(1200, 700)
        self.setStyleSheet(STYLE_SHEET)  # Apply global styles

        # ======== TOP NAVBAR ========
        navbar_layout = QHBoxLayout()
        navbar_layout.setSpacing(15)  # Space between buttons

        # Navigation Buttons
        self.buttons = {
            "Appointments": QPushButton("Appointments"),
            "Clients": QPushButton("Clients"),
            "Billing": QPushButton("Billing"),
            "Treatment": QPushButton("Treatment"),
            "Inventory": QPushButton("Inventory"),
            "Staff": QPushButton("Staff"),
            "Reports": QPushButton("Reports"),
            "Settings": QPushButton("Settings")
        }

        # Styling Buttons
        button_style = """
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                background-color: #f0742f;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #e66727;
                box-shadow: 0px 4px 10px rgba(240, 116, 47, 0.5);
            }
        """

        for btn in self.buttons.values():
            btn.setStyleSheet(button_style)
            navbar_layout.addWidget(btn)

        # Navbar Frame (Border & Padding)
        navbar_frame = QFrame()
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setStyleSheet(
            "background-color: #ffffff; border-bottom: 3px solid #f0742f; padding: 10px;"
        )

        # ======== STACKED WIDGET FOR PAGES ========
        self.stack = QStackedWidget()
        self.pages = {
            "Appointments": AppointmentsPage(),
            "Clients": ClientPage(),
            "Billing": BillingPage(),
            "Treatment": TreatmentPage(),
            "Inventory": InventoryPage(),
            "Staff": StaffPage(),
            "Reports": ReportsPage(),
            "Settings": SettingsPage()
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        # Connect Buttons to Page Switching
        for name, button in self.buttons.items():
            button.clicked.connect(lambda _, page_name=name: self.switch_page(page_name))

        # Set Default Page (Appointments)
        self.switch_page("Appointments")

        # ======== MAIN LAYOUT ========
        main_layout = QVBoxLayout()
        main_layout.addWidget(navbar_frame)  # Top navigation bar
        main_layout.addWidget(self.stack)    # Content area
        self.setLayout(main_layout)

    def switch_page(self, page_name):
        """ Switch to the selected page """
        index = list(self.pages.keys()).index(page_name)
        self.stack.setCurrentIndex(index)


# ======== RUN THE APP ========
if __name__ == "__main__":
    window = DashboardWindow()
    window.show()
    app.exec()
