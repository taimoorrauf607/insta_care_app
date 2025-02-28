from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QHBoxLayout
)
import sqlite3
import os
from PyQt6.QtWidgets import QApplication
from style import STYLE_SHEET  # Import the styles

app = QApplication([])
app.setStyleSheet(STYLE_SHEET)  # Apply global styles


class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.resize(600, 400)

        # Ensure database and table exist
        self.ensure_db()

        # Title
        self.label = QLabel("Inventory Stock:")

        # Table to show stock
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Product", "Stock", "Status"])

        # Input Fields
        self.input_product = QLineEdit()
        self.input_product.setPlaceholderText("Enter Product Name")
        
        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Enter Stock Quantity")

        # Buttons
        self.button_add = QPushButton("Add Product")
        self.button_add.clicked.connect(self.add_product)

        self.button_refresh = QPushButton("Refresh Inventory")
        self.button_refresh.clicked.connect(self.load_inventory)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Product Name:"))
        form_layout.addWidget(self.input_product)

        form_layout2 = QHBoxLayout()
        form_layout2.addWidget(QLabel("Stock Quantity:"))
        form_layout2.addWidget(self.input_stock)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_refresh)

        layout.addLayout(form_layout)
        layout.addLayout(form_layout2)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_inventory()

    def ensure_db(self):
        """Ensures that the inventory table exists in the database."""
        if not os.path.exists("db"):
            os.makedirs("db")  # Create the folder if it doesn't exist

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                stock INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def load_inventory(self):
        """Loads inventory records into the table."""
        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock FROM inventory")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row, (name, stock) in enumerate(records):
            status = "Low Stock" if stock < 5 else "Available"
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(stock)))
            self.table.setItem(row, 2, QTableWidgetItem(status))

    def add_product(self):
        """Adds a new product to the inventory."""
        product = self.input_product.text().strip()
        stock = self.input_stock.text().strip()

        if not product or not stock:
            QMessageBox.warning(self, "Error", "Please enter both Product Name and Stock Quantity!")
            return

        try:
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Error", "Stock must be a valid number!")
            return

        conn = sqlite3.connect("db/crm.db")
        cursor = conn.cursor()

        # Check if product exists
        cursor.execute("SELECT stock FROM inventory WHERE name = ?", (product,))
        existing_product = cursor.fetchone()

        if existing_product:
            # Update stock if product exists
            new_stock = existing_product[0] + stock
            cursor.execute("UPDATE inventory SET stock = ? WHERE name = ?", (new_stock, product))
        else:
            # Insert new product
            cursor.execute("INSERT INTO inventory (name, stock) VALUES (?, ?)", (product, stock))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Product added/updated successfully!")
        self.load_inventory()
