import sqlite3

# Connect to SQLite database (creates db.sqlite3 if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type TEXT NOT NULL,
    name TEXT NOT NULL,
    roll_number TEXT,
    esim_number TEXT,
    class TEXT,
    section TEXT,
    student_group TEXT,
    attending_classes TEXT,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    unique_id TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    parent_child_id TEXT
);

CREATE TABLE IF NOT EXISTS homework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id TEXT NOT NULL,
    class_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    file_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS uploaded_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard INTEGER NOT NULL,
    unit_title TEXT NOT NULL,
    test_date DATE NOT NULL,
    file_name TEXT
);

CREATE TABLE IF NOT EXISTS test_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    unit_title TEXT NOT NULL,
    standard INTEGER NOT NULL,
    submitted_at DATETIME NOT NULL,
    marks INTEGER
);

CREATE TABLE IF NOT EXISTS homework_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    homework_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    parent_id INTEGER,

    FOREIGN KEY (homework_id) REFERENCES homework(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (parent_id) REFERENCES users(id)
);
""")

# Commit changes and close the connection
conn.commit()
conn.close()

print("All tables created successfully in db.sqlite3.")
