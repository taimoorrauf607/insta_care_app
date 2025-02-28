import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
)
from PyQt6.QtWidgets import QApplication
from style import STYLE_SHEET  # Import the styles

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles


class StaffPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Staff Management")
        self.label = QLabel("Staff Records")

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Role", "Salary"])

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Name")

        self.input_role = QLineEdit()
        self.input_role.setPlaceholderText("Role")

        self.input_salary = QLineEdit()
        self.input_salary.setPlaceholderText("Salary")

        self.button_add = QPushButton("Add Staff")
        self.button_add.clicked.connect(self.add_staff)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_role)
        layout.addWidget(self.input_salary)
        layout.addWidget(self.button_add)

        self.setLayout(layout)
        self.load_staff()

    def load_staff(self):
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, role, salary FROM staff")
        staff = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(staff))
        for row, (name, role, salary) in enumerate(staff):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(role))
            self.table.setItem(row, 2, QTableWidgetItem(str(salary)))

    def add_staff(self):
        name = self.input_name.text()
        role = self.input_role.text()
        salary = self.input_salary.text()

        if not name or not role or not salary:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO staff (name, role, salary) VALUES (?, ?, ?)", (name, role, salary))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Staff member added!")
        self.load_staff()
