from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,QApplication
import sqlite3

from style import STYLE_SHEET  # Import the styles

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles

class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reports & Analytics")
        self.resize(600, 400)

        self.label = QLabel("Business Reports:")

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Report Type", "Value", "Date"])

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_reports()

    def load_reports(self):
        """Loads reports from the database."""
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        
        # ✅ Updated column name from `type` → `report_type`
        cursor.execute("SELECT report_type, value, date FROM reports")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row, (rtype, value, date) in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(rtype))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))
            self.table.setItem(row, 2, QTableWidgetItem(date))

