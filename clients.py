from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QTextEdit, QComboBox, QFileDialog, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sqlite3


class ClientPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clients")
        self.resize(900, 600)

        # Initialize database
        self.init_db()

        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Client Management Section")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        main_layout.addWidget(title)

        # **Client Search Bar**
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Clients...")
        self.search_bar.textChanged.connect(self.filter_clients)
        main_layout.addWidget(self.search_bar)

        # **Client Table**
        self.client_table = QTableWidget(0, 5)
        self.client_table.setHorizontalHeaderLabels(["Client Name", "Membership", "Sessions Left", "Date Joined", "Actions"])
        main_layout.addWidget(self.client_table)

        # **Form to Add New Clients**
        form_layout = QVBoxLayout()

        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText("Enter Client Name")
        form_layout.addWidget(self.client_name)

        self.client_history = QTextEdit()
        self.client_history.setPlaceholderText("Enter Medical & Treatment History")
        form_layout.addWidget(self.client_history)

        self.membership_status = QComboBox()
        self.membership_status.addItems(["None", "Silver", "Gold", "Platinum"])
        form_layout.addWidget(self.membership_status)

        self.sessions_left = QLineEdit()
        self.sessions_left.setPlaceholderText("Enter Number of Sessions Left")
        form_layout.addWidget(self.sessions_left)

        self.date_joined = QLineEdit()
        self.date_joined.setPlaceholderText("Enter Date Joined (DD-MM-YYYY)")
        form_layout.addWidget(self.date_joined)

        # **Before/After Photo Upload**
        self.upload_button = QPushButton("Upload Before/After Photos")
        self.upload_button.clicked.connect(self.upload_photo)
        form_layout.addWidget(self.upload_button)  

        # **Save Client Button**
        self.add_client_button = QPushButton("Add Client")
        self.add_client_button.setStyleSheet("background-color: #f0742f; color: white; font-weight: bold;")
        self.add_client_button.clicked.connect(self.add_client)
        form_layout.addWidget(self.add_client_button)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # Load clients from database
        self.populate_clients()

    ### **Initialize Database**
    def init_db(self):
        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                history TEXT,
                membership TEXT,
                sessions INTEGER,
                date_joined TEXT,
                photo BLOB
            )
        """)
        connection.commit()
        connection.close()

    ### **1️⃣ Upload Photo**
    def upload_new_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload New Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            with open(file_path, "rb") as file:
                self.new_image_data = file.read()  # Store new image data
            pixmap = QPixmap(file_path)
            self.photo_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            with open(file_path, "rb") as file:
                self.image_data = file.read()  # Store binary image data
            print(f"Photo uploaded: {file_path}")


    ### **2️⃣ Add New Client (Saves in DB)**
    def add_client(self):
        name = self.client_name.text()
        history = self.client_history.toPlainText()
        membership = self.membership_status.currentText()
        sessions = self.sessions_left.text()
        date_joined = self.date_joined.text()

        if not name or not sessions.isdigit():
            print("Error: Name and sessions must be valid!")
            return

        # Insert into database
        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO clients (name, history, membership, sessions, date_joined, photo) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, history, membership, sessions, date_joined, getattr(self, "image_data", None)))
        connection.commit()
        connection.close()

        # Reload table
        self.populate_clients()

    ### **3️⃣ Search Clients**
    def filter_clients(self):
        query = self.search_bar.text().lower()
        for row in range(self.client_table.rowCount()):
            item = self.client_table.item(row, 0)  # Get client name column
            self.client_table.setRowHidden(row, item is None or query not in item.text().lower())

    ### **4️⃣ Populate Table from DB**
    def populate_clients(self):
        self.client_table.setRowCount(0)  # Clear table first

        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, membership, sessions, date_joined FROM clients")
        clients = cursor.fetchall()
        connection.close()

        for row, (client_id, name, membership, sessions, date_joined) in enumerate(clients):
            self.client_table.insertRow(row)
            self.client_table.setItem(row, 0, QTableWidgetItem(name))
            self.client_table.setItem(row, 1, QTableWidgetItem(membership))
            self.client_table.setItem(row, 2, QTableWidgetItem(str(sessions)))
            self.client_table.setItem(row, 3, QTableWidgetItem(date_joined))

            # **Edit Button**
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, r=row: self.edit_client(r))
            self.client_table.setCellWidget(row, 4, edit_button)
    def save_client_changes(self, row, name_field, membership_field, sessions_field, date_joined_field, dialog):
        new_name = name_field.text()
        new_membership = membership_field.currentText()
        new_sessions = sessions_field.text()
        new_date_joined = date_joined_field.text()

        if not new_name or not new_sessions.isdigit():
            print("Error: Name and sessions must be valid!")
            return

        client_id = self.get_client_id_by_row(row)

        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        if self.new_image_data:  # If a new photo was uploaded
            cursor.execute("""
                UPDATE clients SET name=?, membership=?, sessions=?, date_joined=?, photo=? WHERE id=?
            """, (new_name, new_membership, new_sessions, new_date_joined, self.new_image_data, client_id))
        else:
            cursor.execute("""
                UPDATE clients SET name=?, membership=?, sessions=?, date_joined=? WHERE id=?
            """, (new_name, new_membership, new_sessions, new_date_joined, client_id))

        connection.commit()
        connection.close()

        dialog.accept()  # Close the dialog
        self.populate_clients()  # Refresh the table

    def get_client_id_by_row(self, row):
        client_name = self.client_table.item(row, 0).text()
        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM clients WHERE name=?", (client_name,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None


    ### **5️⃣ Edit Client**
    def edit_client(self, row):
        client_name = self.client_table.item(row, 0).text()
        membership = self.client_table.item(row, 1).text()
        sessions = self.client_table.item(row, 2).text()
        date_joined = self.client_table.item(row, 3).text()

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit Client: {client_name}")
        dialog.resize(400, 400)

        layout = QFormLayout()

        name_field = QLineEdit(client_name)
        membership_field = QComboBox()
        membership_field.addItems(["None", "Silver", "Gold", "Platinum"])
        membership_field.setCurrentText(membership)

        sessions_field = QLineEdit(sessions)
        date_joined_field = QLineEdit(date_joined)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px solid black;")

        connection = sqlite3.connect("crm.db")
        cursor = connection.cursor()
        cursor.execute("SELECT photo FROM clients WHERE name=?", (client_name,))
        result = cursor.fetchone()
        connection.close()

        self.new_image_data = None  

        if result and result[0]:  
            pixmap = QPixmap()
            pixmap.loadFromData(result[0])
            self.photo_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        upload_photo_btn = QPushButton("Upload New Photo")
        upload_photo_btn.clicked.connect(self.upload_new_photo)

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(lambda: self.save_client_changes(row, name_field, membership_field, sessions_field, date_joined_field, dialog))

        layout.addRow("Name:", name_field)
        layout.addRow("Membership:", membership_field)
        layout.addRow("Sessions Left:", sessions_field)
        layout.addRow("Date Joined:", date_joined_field)
        layout.addRow("Photo:", self.photo_label)
        layout.addWidget(upload_photo_btn)
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec()
