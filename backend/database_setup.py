import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Create bookings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    seat_number TEXT,
    passenger_name TEXT,
    age INTEGER,
    gender TEXT,
    payment_method TEXT,
    amount REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Database and tables created successfully!")
