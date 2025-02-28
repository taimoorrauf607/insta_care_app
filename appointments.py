from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QDateEdit, QTimeEdit, QHBoxLayout, QApplication
)
from PyQt6.QtCore import QDate, QTime, Qt
import sqlite3

class AppointmentsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Appointments")
        self.label = QLabel("Appointments List")

        # Table with all appointment details + Delete Button Column
        self.table = QTableWidget(0, 8)  # 8 columns (7 details + 1 delete button)
        self.table.setHorizontalHeaderLabels(["Token", "Client Name", "Phone", "Date", "Time", "Doctor", "Details", "Action"])

        # Input Fields
        self.input_client = QLineEdit()
        self.input_client.setPlaceholderText("Client Name")
        self.input_client.returnPressed.connect(self.focus_phone)  # Move cursor to phone

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Phone Number")
        self.input_phone.returnPressed.connect(self.focus_date)  # Move cursor to date

        # Date Selector (QDateEdit) → Use `editingFinished` Instead of `returnPressed`
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        self.input_date.editingFinished.connect(self.focus_time)  # Move cursor to time
        self.input_date.installEventFilter(self)  # Capture "Enter" key

        # Time Selector (QTimeEdit) → Use `editingFinished`
        self.input_time = QTimeEdit()
        self.input_time.setTime(QTime.currentTime())
        self.input_time.editingFinished.connect(self.focus_doctor)  # Move cursor to doctor
        self.input_time.installEventFilter(self)  # Capture "Enter" key

        self.input_doctor = QLineEdit()
        self.input_doctor.setPlaceholderText("Doctor Name")
        self.input_doctor.returnPressed.connect(self.focus_details)  # Move cursor to details

        self.input_details = QLineEdit()
        self.input_details.setPlaceholderText("Details")
        self.input_details.returnPressed.connect(self.add_appointment)  # Add appointment

        # Add Button
        self.button_add = QPushButton("Add Appointment")
        self.button_add.clicked.connect(self.add_appointment)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Client Name:"))
        form_layout.addWidget(self.input_client)
        form_layout.addWidget(QLabel("Phone Number:"))
        form_layout.addWidget(self.input_phone)
        form_layout.addWidget(QLabel("Date:"))
        form_layout.addWidget(self.input_date)
        form_layout.addWidget(QLabel("Time:"))
        form_layout.addWidget(self.input_time)
        form_layout.addWidget(QLabel("Doctor Name:"))
        form_layout.addWidget(self.input_doctor)
        form_layout.addWidget(QLabel("Details:"))
        form_layout.addWidget(self.input_details)

        form_layout.addWidget(self.button_add)

        layout.addLayout(form_layout)
        self.setLayout(layout)

        self.load_appointments()

    # Focus Functions for Enter Key Handling
    def focus_phone(self):
        self.input_phone.setFocus()

    def focus_date(self):
        self.input_date.setFocus()

    def focus_time(self):
        self.input_time.setFocus()

    def focus_doctor(self):
        self.input_doctor.setFocus()

    def focus_details(self):
        self.input_details.setFocus()

    def load_appointments(self):
        """Loads appointments from the database and adds delete buttons."""
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_name, phone_number, date, time, doctor_name, details FROM appointments")
        appointments = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(appointments))
        for row, (token, client, phone, date, time, doctor, details) in enumerate(appointments):
            self.table.setItem(row, 0, QTableWidgetItem(str(token)))
            self.table.setItem(row, 1, QTableWidgetItem(client))
            self.table.setItem(row, 2, QTableWidgetItem(phone))
            self.table.setItem(row, 3, QTableWidgetItem(date))
            self.table.setItem(row, 4, QTableWidgetItem(time))
            self.table.setItem(row, 5, QTableWidgetItem(doctor))
            self.table.setItem(row, 6, QTableWidgetItem(details))

            # Add Delete Button
            delete_button = QPushButton("🗑 Delete")
            delete_button.clicked.connect(lambda _, t=token: self.delete_appointment(t))
            self.table.setCellWidget(row, 7, delete_button)

    def add_appointment(self):
        """Adds a new appointment and clears input fields."""
        client_name = self.input_client.text().strip()
        phone_number = self.input_phone.text().strip()
        date = self.input_date.date().toString("dd-MMM-yyyy")
        time = self.input_time.time().toString("hh:mm AP")
        doctor_name = self.input_doctor.text().strip()
        details = self.input_details.text().strip()

        if not client_name or not phone_number or not doctor_name or not details:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (client_name, phone_number, date, time, doctor_name, details) VALUES (?, ?, ?, ?, ?, ?)",
            (client_name, phone_number, date, time, doctor_name, details)
        )
        conn.commit()
        conn.close()

        self.clear_inputs()
        QMessageBox.information(self, "Success", "Appointment added!")
        self.load_appointments()

    def delete_appointment(self, token):
        """Deletes an appointment when the delete button is clicked."""
        confirmation = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this appointment?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("db/crm.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE id = ?", (token,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Appointment deleted!")
            self.load_appointments()  # Refresh table

    def clear_inputs(self):
        """Clears input fields after adding an appointment."""
        self.input_client.clear()
        self.input_phone.clear()
        self.input_date.setDate(QDate.currentDate())
        self.input_time.setTime(QTime.currentTime())
        self.input_doctor.clear()
        self.input_details.clear()

    def eventFilter(self, obj, event):
        """Handles Enter key in QDateEdit and QTimeEdit."""
        if event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            if obj == self.input_date:
                self.focus_time()
                return True
            elif obj == self.input_time:
                self.focus_doctor()
                return True
        return super().eventFilter(obj, event)


# Run the App (for testing)
if __name__ == "__main__":
    app = QApplication([])
    window = AppointmentsPage()
    window.show()
    app.exec()
