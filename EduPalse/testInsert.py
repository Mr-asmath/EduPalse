"""import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

user_type = "Teacher"  # Must match allowed CHECK values
name = "John "
attending_classes = "Math"
email = "john2@example.com"
phone = "1234567290"
unique_id = "Y001"
password = "hashedpassword"

print("About to insert:", user_type, name, attending_classes, email, phone, unique_id, password)

cursor.execute("
    INSERT INTO users (user_type, name, attending_classes, email, phone, unique_id, password)
  VALUES (?, ?, ?, ?, ?, ?, ?)
", (user_type, name, attending_classes, email, phone, unique_id, password))

conn.commit()"""

import sqlite3
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
cursor.execute("select * from users")
print(cursor.fetchall())

