import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QHeaderView, QComboBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Billing Section')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        table_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Header
        header_label = QLabel('BILLING SECTION')
        header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        header_label.setStyleSheet('color: red;')
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Form Fields
        client_name_label = QLabel('Client Name:')
        self.client_name_input = QLineEdit()

        product_label = QLabel('Product:')
        self.product_input = QLineEdit()

        quantity_label = QLabel('Quantity:')
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)

        price_label = QLabel('Price:')
        self.price_input = QLineEdit()

        form_layout.addWidget(client_name_label)
        form_layout.addWidget(self.client_name_input)
        form_layout.addWidget(product_label)
        form_layout.addWidget(self.product_input)
        form_layout.addWidget(quantity_label)
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(price_label)
        form_layout.addWidget(self.price_input)

        main_layout.addLayout(form_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Product', 'Quantity', 'Price', 'Total', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table)

        # Buttons
        add_button = QPushButton('ADD')
        add_button.setStyleSheet('background-color: green; color: white; font-weight: bold;')
        add_button.clicked.connect(self.add_product)
        save_button = QPushButton('SAVE')
        cancel_button = QPushButton('CANCEL')

        button_layout.addWidget(add_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(table_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_product(self):
        product_name = self.product_input.text()
        quantity = self.quantity_input.value()
        price = self.price_input.text()

        if not product_name or not price:
            QMessageBox.warning(self, 'Input Error', 'Please provide all product details.')
            return

        try:
            price = float(price)
            total = quantity * price
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(product_name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
            self.table.setItem(row_position, 2, QTableWidgetItem(f'{price:.2f}'))
            self.table.setItem(row_position, 3, QTableWidgetItem(f'{total:.2f}'))
            remove_button = QPushButton('Remove')
            remove_button.setStyleSheet('background-color: red; color: white;')
            remove_button.clicked.connect(lambda: self.table.removeRow(row_position))
            self.table.setCellWidget(row_position, 4, remove_button)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Price must be a number.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = inventory()
    window.show()
    sys.exit(app.exec())
