from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, 
    QFrame, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QTextEdit
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QDateEdit
class AppointmentsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        main_layout = QHBoxLayout()

        # Sidebar Layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)

        self.sidebar_buttons = {
            "Book Appointment": QPushButton("Book Appointment"),
            "Upcoming Appointments": QPushButton("Upcoming"),
            "Waitlist": QPushButton("Waitlist"),
            "Recurring Appointments": QPushButton("Recurring"),
            "Multi-Location Scheduling": QPushButton("Multi-Location")
        }

        # Sidebar Styling
        for btn in self.sidebar_buttons.values():
            btn.setStyleSheet(
                "QPushButton { padding: 10px; border-radius: 5px; background-color: #f0742f; color: white; font-size: 14px; font-weight: bold; border: none; transition: all 0.3s ease; }"
                "QPushButton:hover { background-color: #e66727; box-shadow: 0px 4px 10px rgba(240, 116, 47, 0.5); }"
            )
            sidebar_layout.addWidget(btn)

        # Sidebar Frame
        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar_layout)
        sidebar_frame.setStyleSheet("background-color: #ffffff; border-right: 3px solid #f0742f; padding: 10px;")

        # Stacked Widget for Pages
        self.stack = QStackedWidget()

        # Add Pages
        self.stack.addWidget(self.create_book_appointment_page())  
        self.stack.addWidget(self.create_upcoming_appointments_page())  
        self.stack.addWidget(self.create_waitlist_page())  
        self.stack.addWidget(self.create_recurring_appointments_page())  

        # Connect Sidebar Buttons to Stack
        for i, (name, button) in enumerate(self.sidebar_buttons.items()):
            button.clicked.connect(lambda _, index=i: self.stack.setCurrentIndex(index))

        # Default Page
        self.stack.setCurrentIndex(0)

        # Add Sidebar & Content to Main Layout
        main_layout.addWidget(sidebar_frame, 1)  # Sidebar (Fixed Width)
        main_layout.addWidget(self.stack, 4)  # Main Content (Flexible)

        self.setLayout(main_layout)

    ### **1. Book Appointment Page**
    def create_book_appointment_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Book New Appointment"))

        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText("Enter Client Name")
        layout.addWidget(self.client_name)

        self.treatment_type = QComboBox()
        self.treatment_type.addItems(["Botox", "Fillers", "Laser", "Facial"])
        layout.addWidget(self.treatment_type)

        # Replace QLineEdit with QDateEdit for the date input
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Enable calendar popup
        self.date_input.setDate(QDate.currentDate())  # Set default date to today
        self.date_input.setDisplayFormat("dd-MM-yyyy")  # Format the displayed date
        layout.addWidget(self.date_input)

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Additional Notes")
        layout.addWidget(self.notes)

        book_button = QPushButton("Book Appointment")
        book_button.setStyleSheet("background-color: #f0742f; color: white;")
        book_button.clicked.connect(self.book_appointment)
        layout.addWidget(book_button)

        page.setLayout(layout)
        return page


    def book_appointment(self):
        name = self.client_name.text()
        treatment = self.treatment_type.currentText()
        date = self.date_input.date().toString("dd-MM-yyyy")  # Get date as a string
        notes = self.notes.toPlainText()
        print(f"Appointment booked for {name} on {date} for {treatment} (Notes: {notes})")


    ### **2. Upcoming Appointments Page**
    def create_upcoming_appointments_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Upcoming Appointments"))

        self.search_upcoming = QLineEdit()
        self.search_upcoming.setPlaceholderText("Search Appointment...")
        self.search_upcoming.textChanged.connect(lambda: self.filter_table(self.upcoming_table, self.search_upcoming.text()))
        layout.addWidget(self.search_upcoming)

        self.upcoming_table = QTableWidget(5, 3)
        self.upcoming_table.setHorizontalHeaderLabels(["Client Name", "Date", "Treatment"])
        self.populate_upcoming_table()
        layout.addWidget(self.upcoming_table)

        page.setLayout(layout)
        return page

    def populate_upcoming_table(self):
        data = [
            ("John Doe", "10-03-2025", "Laser"),
            ("Emma Smith", "15-03-2025", "Fillers"),
            ("Michael Brown", "20-03-2025", "Botox"),
        ]
        self.upcoming_table.setRowCount(len(data))
        for row, (name, date, treatment) in enumerate(data):
            self.upcoming_table.setItem(row, 0, QTableWidgetItem(name))
            self.upcoming_table.setItem(row, 1, QTableWidgetItem(date))
            self.upcoming_table.setItem(row, 2, QTableWidgetItem(treatment))

    ### **3. Waitlist Page**
    def create_waitlist_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Waitlist Management"))

        self.search_waitlist = QLineEdit()
        self.search_waitlist.setPlaceholderText("Search Waitlist...")
        self.search_waitlist.textChanged.connect(lambda: self.filter_table(self.waitlist_table, self.search_waitlist.text()))
        layout.addWidget(self.search_waitlist)

        self.waitlist_table = QTableWidget(3, 3)
        self.waitlist_table.setHorizontalHeaderLabels(["Client Name", "Priority", "Notes"])
        self.populate_waitlist_table()
        layout.addWidget(self.waitlist_table)

        page.setLayout(layout)
        return page

    def populate_waitlist_table(self):
        data = [
            ("Jane Doe", "High", "Wants earlier slot"),
            ("Alex Carter", "Medium", "Flexible schedule"),
        ]
        self.waitlist_table.setRowCount(len(data))
        for row, (name, priority, notes) in enumerate(data):
            self.waitlist_table.setItem(row, 0, QTableWidgetItem(name))
            self.waitlist_table.setItem(row, 1, QTableWidgetItem(priority))
            self.waitlist_table.setItem(row, 2, QTableWidgetItem(notes))

    ### **4. Recurring Appointments Page**
    def create_recurring_appointments_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Recurring Appointments"))

        self.search_recurring = QLineEdit()
        self.search_recurring.setPlaceholderText("Search Recurring Appointments...")
        self.search_recurring.textChanged.connect(lambda: self.filter_table(self.recurring_table, self.search_recurring.text()))
        layout.addWidget(self.search_recurring)

        self.recurring_table = QTableWidget(2, 3)
        self.recurring_table.setHorizontalHeaderLabels(["Client Name", "Interval", "Next Session"])
        self.populate_recurring_table()
        layout.addWidget(self.recurring_table)

        page.setLayout(layout)
        return page

    def populate_recurring_table(self):
        data = [
            ("Sarah Lee", "Every 2 Weeks", "20-03-2025"),
        ]
        self.recurring_table.setRowCount(len(data))
        for row, (name, interval, next_session) in enumerate(data):
            self.recurring_table.setItem(row, 0, QTableWidgetItem(name))
            self.recurring_table.setItem(row, 1, QTableWidgetItem(interval))
            self.recurring_table.setItem(row, 2, QTableWidgetItem(next_session))

    ### **🔍 Search Filtering Function**
    def filter_table(self, table, query):
        query = query.lower()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            table.setRowHidden(row, item is None or query not in item.text().lower())
