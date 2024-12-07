import sqlite3
import os

# Ensure the instance folder exists
os.makedirs('instance', exist_ok=True)

# Path to the database
db_path = 'instance/users.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
print(f"Database created at {db_path}")

# Commit and close the connection
conn.commit()
conn.close()
