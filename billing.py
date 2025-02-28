import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QDateEdit, QApplication
)
from PyQt6.QtCore import QDate, Qt


class BillingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Billing & Payments")
        self.resize(700, 500)

        # Title Label
        self.label = QLabel("Billing & Payments")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Billing Table
        self.table = QTableWidget(0, 6)  # 6 columns (5 details + 1 delete button)
        self.table.setHorizontalHeaderLabels(["Client Name", "Amount", "Status", "Method", "Date", "Action"])
        self.table.setColumnWidth(0, 150)  # Client Name
        self.table.setColumnWidth(1, 100)  # Amount
        self.table.setColumnWidth(2, 100)  # Status
        self.table.setColumnWidth(3, 150)  # Method
        self.table.setColumnWidth(4, 120)  # Date
        self.table.setColumnWidth(5, 80)   # Action

        # Input Fields
        self.input_client = QLineEdit()
        self.input_client.setPlaceholderText("Client Name")
        self.input_client.returnPressed.connect(self.focus_amount)

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Enter Amount")
        self.input_amount.returnPressed.connect(self.focus_status)

        self.combo_status = QComboBox()
        self.combo_status.addItems(["Paid", "Unpaid", "Pending"])
        self.combo_status.currentIndexChanged.connect(self.focus_method)

        self.combo_method = QComboBox()
        self.combo_method.addItems(["Credit/Debit Card", "Mobile Wallet", "Cash", "Installments"])
        self.combo_method.currentIndexChanged.connect(self.focus_date)

        # Date Selector
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())
        self.input_date.editingFinished.connect(self.focus_add_button)
        self.input_date.installEventFilter(self)

        # Add Button
        self.button_add = QPushButton("Add Billing Entry")
        self.button_add.setStyleSheet("background-color: #007bff; color: white; padding: 6px;")
        self.button_add.clicked.connect(self.add_billing)

        # Layouts for Inputs
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Client Name:"))
        form_layout.addWidget(self.input_client)
        form_layout.addWidget(QLabel("Amount:"))
        form_layout.addWidget(self.input_amount)
        form_layout.addWidget(QLabel("Status:"))
        form_layout.addWidget(self.combo_status)
        form_layout.addWidget(QLabel("Payment Method:"))
        form_layout.addWidget(self.combo_method)
        form_layout.addWidget(QLabel("Date:"))
        form_layout.addWidget(self.input_date)
        form_layout.addWidget(self.button_add)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.table)
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)
        self.load_billing()

    def load_billing(self):
        """Loads billing records from the database and adds delete buttons."""
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_name, amount, status, method, date FROM billing")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row, (billing_id, client, amount, status, method, date) in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(client))
            self.table.setItem(row, 1, QTableWidgetItem(f"Rs.{amount:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(status))
            self.table.setItem(row, 3, QTableWidgetItem(method))
            self.table.setItem(row, 4, QTableWidgetItem(date))

            # Add Delete Button
            delete_button = QPushButton("🗑 Delete")
            delete_button.clicked.connect(lambda _, b_id=billing_id: self.delete_billing(b_id))
            self.table.setCellWidget(row, 5, delete_button)

    def add_billing(self):
        """Adds a new billing entry and clears input fields."""
        client_name = self.input_client.text().strip()
        amount = self.input_amount.text().strip()
        status = self.combo_status.currentText()
        method = self.combo_method.currentText()
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
        cursor.execute(
            "INSERT INTO billing (client_name, amount, status, method, date) VALUES (?, ?, ?, ?, ?)",
            (client_name, amount, status, method, date)
        )
        conn.commit()
        conn.close()

        self.clear_inputs()
        QMessageBox.information(self, "Success", "Billing entry added!")
        self.load_billing()

    def delete_billing(self, billing_id):
        """Deletes a billing entry when the delete button is clicked."""
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

            QMessageBox.information(self, "Success", "Billing record deleted!")
            self.load_billing()  # Refresh table

    def clear_inputs(self):
        """Clears input fields after adding a billing entry."""
        self.input_client.clear()
        self.input_amount.clear()
        self.input_date.setDate(QDate.currentDate())

    # 🔽 Keyboard Navigation Functions 🔽
    def focus_amount(self):
        self.input_amount.setFocus()

    def focus_status(self):
        self.combo_status.setFocus()

    def focus_method(self):
        self.combo_method.setFocus()

    def focus_date(self):
        self.input_date.setFocus()

    def focus_add_button(self):
        self.button_add.setFocus()

    def eventFilter(self, obj, event):
        """Handles Enter key in QDateEdit."""
        if event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            if obj == self.input_date:
                self.focus_add_button()
                return True
        return super().eventFilter(obj, event)


# Run the App (for testing)
if __name__ == "__main__":
    app = QApplication([])
    window = BillingPage()
    window.show()
    app.exec()
