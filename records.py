from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QMessageBox, QHBoxLayout
)
import sqlite3
from PyQt6.QtWidgets import QApplication
from style import STYLE_SHEET  # Import the styles

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles


class RecordsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client Records")
        self.resize(500, 400)

        # UI Elements
        self.label = QLabel("Stored Client Records:")

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Record Name", "Details"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 300)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Enter Record Name")

        self.input_details = QLineEdit()
        self.input_details.setPlaceholderText("Enter Record Details")

        self.button_add = QPushButton("Add Record")
        self.button_add.clicked.connect(self.add_record)

        self.button_delete = QPushButton("Delete Selected")
        self.button_delete.clicked.connect(self.delete_record)

        # Layouts
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_details)
        form_layout.addWidget(self.button_add)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        layout.addLayout(form_layout)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

        self.load_records()

    def load_records(self):
        """Load records from the database and display them in the table."""
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, details FROM records")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row, (record_id, name, details) in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(details))
            self.table.setItem(row, 2, QTableWidgetItem(str(record_id)))  # Hidden column for ID

    def add_record(self):
        """Add a new record to the database."""
        name = self.input_name.text().strip()
        details = self.input_details.text().strip()

        if not name or not details:
            QMessageBox.warning(self, "Input Error", "Both fields are required!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO records (name, details) VALUES (?, ?)", (name, details))
        conn.commit()
        conn.close()

        self.input_name.clear()
        self.input_details.clear()
        self.load_records()

    def delete_record(self):
        """Delete selected record from the database."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a record to delete.")
            return

        record_name = self.table.item(selected_row, 0).text()
        confirmation = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete '{record_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("db/crm.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE name=?", (record_name,))
            conn.commit()
            conn.close()

            self.load_records()

