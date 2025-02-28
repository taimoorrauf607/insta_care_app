from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QApplication
)
from appointments import AppointmentsPage
from billing import BillingPage
from inventory import InventoryPage
from staff import StaffPage
from reports import ReportsPage
from records import RecordsPage
from style import STYLE_SHEET  # Import the styles

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRM Dashboard")
        self.resize(800, 600)

        # Sidebar buttons
        sidebar_layout = QVBoxLayout()
        self.button_appointments = QPushButton("Appointments")
        self.button_billing = QPushButton("Billing")
        self.button_inventory = QPushButton("Inventory")
        self.button_staff = QPushButton("Staff")
        self.button_reports = QPushButton("Reports")
        self.button_records = QPushButton("Records")

        # Adding buttons to sidebar
        for button in [
            self.button_appointments, self.button_billing, self.button_inventory,
            self.button_staff, self.button_reports, self.button_records
        ]:
            sidebar_layout.addWidget(button)

        # Create a stacked widget for pages
        self.stack = QStackedWidget()
        self.appointments_page = AppointmentsPage()
        self.billing_page = BillingPage()
        self.inventory_page = InventoryPage()
        self.staff_page = StaffPage()
        self.reports_page = ReportsPage()
        self.records_page = RecordsPage()

        # Add pages to the stack
        self.stack.addWidget(self.appointments_page)  # Index 0
        self.stack.addWidget(self.billing_page)       # Index 1
        self.stack.addWidget(self.inventory_page)     # Index 2
        self.stack.addWidget(self.staff_page)         # Index 3
        self.stack.addWidget(self.reports_page)       # Index 4
        self.stack.addWidget(self.records_page)       # Index 5

        # Connect buttons to page switching
        self.button_appointments.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.button_billing.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.button_inventory.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.button_staff.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.button_reports.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.button_records.clicked.connect(lambda: self.stack.setCurrentIndex(5))

        # Layout
        layout = QHBoxLayout()
        layout.addLayout(sidebar_layout)
        layout.addWidget(self.stack)

        self.setLayout(layout)
