import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QDateEdit, QApplication
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate, Qt

from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class BillingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Billing & Payments")
        self.resize(800, 600)

        # Title Label
        self.label = QLabel("Billing & Payments")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Billing Table
        self.table = QTableWidget(0, 7)  
        self.table.setHorizontalHeaderLabels(["Client Name", "Amount", "Status", "Method", "Discount", "Date", "Action"])

        # Input Fields
        self.input_client = QLineEdit()
        self.input_client.setPlaceholderText("Client Name")
        self.input_client.returnPressed.connect(self.focus_amount)

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Enter Amount")
        self.input_amount.returnPressed.connect(self.focus_status)

        self.combo_status = QComboBox()
        self.combo_status.addItems(["Paid", "Unpaid", "Pending"])

        self.combo_method = QComboBox()
        self.combo_method.addItems(["Credit/Debit Card", "Mobile Wallet", "Cash", "Installments"])

        self.combo_packages = QComboBox()
        self.combo_packages.addItems(["Basic Package", "Premium Package", "VIP Package"])

        self.input_discount = QLineEdit()
        self.input_discount.setPlaceholderText("Discount (%)")
        self.input_discount.setValidator(QIntValidator(0, 100))

        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())

        # Add Button
        self.button_add = QPushButton("Add Billing Entry")
        self.button_add.setStyleSheet("background-color: #007bff; color: white; padding: 6px;")
        self.button_add.clicked.connect(self.add_billing)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 120))  # Light shadow
        self.button_add.setGraphicsEffect(shadow)

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.label)
        form_layout.addWidget(self.table)
        form_layout.addWidget(self.input_client)
        form_layout.addWidget(self.input_amount)
        form_layout.addWidget(self.combo_status)
        form_layout.addWidget(self.combo_method)
        form_layout.addWidget(self.combo_packages)
        form_layout.addWidget(self.input_discount)
        form_layout.addWidget(self.input_date)
        form_layout.addWidget(self.button_add)

        self.setLayout(form_layout)
        self.load_billing()

    def focus_amount(self):
        self.input_amount.setFocus()
    def focus_status(self):
        self.combo_status.setFocus()



    def load_billing(self):
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_name, amount, status, method, discount, date FROM billing")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row, (billing_id, client, amount, status, method, discount, date) in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(client))
            self.table.setItem(row, 1, QTableWidgetItem(f"Rs.{amount:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(status))
            self.table.setItem(row, 3, QTableWidgetItem(method))
            self.table.setItem(row, 4, QTableWidgetItem(f"{discount}%"))
            self.table.setItem(row, 5, QTableWidgetItem(date))

            delete_button = QPushButton("🗑 Delete")
            delete_button.clicked.connect(lambda _, b_id=billing_id: self.delete_billing(b_id))
            self.table.setCellWidget(row, 6, delete_button)  # Correct column index for Action


    def add_billing(self):
        client_name = self.input_client.text().strip()
        amount = self.input_amount.text().strip()
        status = self.combo_status.currentText()
        method = self.combo_method.currentText()
        package = self.combo_packages.currentText()
        date = self.input_date.date().toString("dd-MMM-yyyy")

        if not client_name or not amount:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a valid number!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM billing WHERE client_name = ?", (client_name,))
        client_count = cursor.fetchone()[0]

        discount = 0
        if client_count >= 2:
            if package == "Basic Package":
                discount = 5
            elif package == "Premium Package":
                discount = 10
            elif package == "VIP Package":
                discount = 15

        discounted_amount = amount - (amount * discount / 100)

        cursor.execute(
            "INSERT INTO billing (client_name, amount, status, method, date, discount) VALUES (?, ?, ?, ?, ?, ?)",
            (client_name, discounted_amount, status, method, date, discount)
        )
        conn.commit()
        conn.close()

        self.clear_inputs()
        QMessageBox.information(self, "Success", "Billing entry added!")
        self.load_billing()



    def delete_billing(self, billing_id):
        confirmation = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this billing record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("db/crm.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM billing WHERE id = ?", (billing_id,))
            conn.commit()
            conn.close()
            self.load_billing()

    def clear_inputs(self):
        self.input_client.clear()
        self.input_amount.clear()
        self.input_discount.clear()
        self.input_date.setDate(QDate.currentDate())

if __name__ == "__main__":
    app = QApplication([])
    window = BillingPage()
    window.show()
    app.exec()




