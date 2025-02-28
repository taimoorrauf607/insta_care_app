import sqlite3
import os

# Ensure the database directory exists
db_path = "db/crm.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def initialize_db():
    """Creates and initializes the database tables if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Appointments Table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Token No.
            client_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            details TEXT NULL
        )
    """)

    # Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL CHECK(stock >= 0)
        )
    """)

    # Staff Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL CHECK(salary >= 0)
        )
    """)

    # Reports Table (Updated column names)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            value REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Records Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            details TEXT
        )
    """)

    # Billing Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            amount REAL,
            status TEXT,
            method TEXT,
            date TEXT
        )
    """)

     

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    initialize_db()


  
