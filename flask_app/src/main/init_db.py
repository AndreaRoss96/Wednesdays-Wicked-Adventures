import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# IMPORTANT: Enable foreign key support in SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# Roles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
)
""")

# Parks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS parks (
    park_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL
)
""")

# Bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    park_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    num_tickets INTEGER NOT NULL DEFAULT 1,
    health_safety INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (park_id) REFERENCES parks(park_id)
)
""")

connection.commit()
connection.close()

print("Database initialized successfully")
