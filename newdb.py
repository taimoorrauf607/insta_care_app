import sqlite3

conn = sqlite3.connect("db/crm.db")
cursor = conn.cursor()

# Add the 'discount' column if it doesn't already exist
try:
    cursor.execute("ALTER TABLE billing ADD COLUMN discount INTEGER DEFAULT 0")
    conn.commit()
    print("Column 'discount' added successfully!")
except sqlite3.OperationalError as e:
    print("Column 'discount' might already exist or an error occurred:", e)

# Check the table structure to verify the column
cursor.execute("PRAGMA table_info(billing)")
columns = cursor.fetchall()
for column in columns:
    print(column)

conn.close()
