import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# -------------------- Insert Parents --------------------
parents = [
    ("Mary", "65784326"),
    ("Kelvin", "65762345"),
    ("Lam", "65711111"),
    ("Rose", "65722222"), 
    ("David", "65733333"),
    ("Irene", "65744444"),
    ("Mason", "65755555"),
    ("Nina", "65766666"),
    ("Henry", "65777777"),
    ("Olivia", "65788888")
]

parent_map = {}
for i, (name, child_unique_id) in enumerate(parents):
    parent_unique_id = f"65145{i:03}"
    email = f"{name.lower()}@gmail.com"
    phone = f"98000001{i+1}"
    password = f"{name.lower()}@123"

    cursor.execute("""
        INSERT INTO users (user_type, name, roll_number, esim_number, class, section, student_group,
        attending_classes, email, phone, unique_id, password, parent_child_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("Parent", name, None, None, "1", "A", None, None, email, phone, parent_unique_id, password, child_unique_id))
    
    parent_map[child_unique_id] = parent_unique_id

# -------------------- Insert Students --------------------
students = [
    ("Student", "Adam", "12001", "9202250104001", "1", "A", None, None, "adam@gmail.com", "9876543210", "65784326", "Adam@123", None),
    ("Student", "Bob", "12002", "9202250104002", "1", "A", None, None, "bob@gmail.com", "9801237643", "65762345", "bob@123", None),
    ("Student", "Dev", "12003", "9202250104003", "1", "A", None, None, "dev@gmail.com", "9875789210", "65711111", "dev@123", None),
    ("Student", "Ema", "12004", "9202250104004", "1", "A", None, None, "ema@gmail.com", "9800000011", "65722222", "ema@123", None),
    ("Student", "Rita", "12005", "9202250104005", "1", "A", None, None, "rita@gmail.com", "9800000012", "65733333", "rita@123", None),
    ("Student", "Liam", "12006", "9202250104006", "1", "A", None, None, "liam@gmail.com", "9800000013", "65744444", "liam@123", None),
    ("Student", "Tina", "12007", "9202250104007", "1", "A", None, None, "tina@gmail.com", "9800000014", "65755555", "tina@123", None),
    ("Student", "Sam", "12008", "9202250104008", "1", "A", None, None, "sam@gmail.com", "9800000015", "65766666", "sam@123", None),
    ("Student", "Arya", "12009", "9202250104009", "1", "A", None, None, "arya@gmail.com", "9800000016", "65777777", "arya@123", None),
    ("Student", "Noah", "12010", "9202250104010", "1", "A", None, None, "noah@gmail.com", "9800000017", "65788888", "noah@123", None)
]

for student in students:
    *base_data, student_unique_id, password, _ = student
    parent_id = parent_map.get(student_unique_id)
    cursor.execute("""
        INSERT INTO users (user_type, name, roll_number, esim_number, class, section, student_group,
        attending_classes, email, phone, unique_id, password, parent_child_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (*base_data, student_unique_id, password, parent_id))

# -------------------- Insert Teachers --------------------
teacher_names = ["Alice", "Brian", "Charles", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"]

for i, name in enumerate(teacher_names):
    attending_classes = ",".join(str(random.randint(1, 12)) for _ in range(random.randint(1, 3)))
    email = f"{name.lower()}@school.com"
    phone = f"99900000{i+1}"
    unique_id = f"TCHR{i+1001}"
    password = f"{name.lower()}@teach"

    cursor.execute("""
        INSERT INTO users (user_type, name, roll_number, esim_number, class, section, student_group,
        attending_classes, email, phone, unique_id, password, parent_child_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("Teacher", name, None, None, None, None, None, attending_classes, email, phone, unique_id, password, None))

# -------------------- Insert Homework --------------------
titles = ["English", "Maths", "Science", "History", "Geography"]
descriptions = ["2 lessons", "Test", "Reading", "Class test", "Write notes"]
homework_id = 1
base_teacher_ids = [f"TCHR100{i}" for i in range(1, 6)]
base_time = datetime(2025, 4, 6, 16, 0, 0)

for standard in range(1, 13):
    for i in range(5):
        teacher_id = random.choice(base_teacher_ids)
        title = titles[i % len(titles)]
        description = descriptions[i % len(descriptions)]
        created_at = base_time + timedelta(minutes=5 * homework_id)

        cursor.execute("""
            INSERT INTO homework (teacher_id, class_name, title, description, file_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (teacher_id, str(standard), title, description, None, created_at.strftime("%Y-%m-%d %H:%M:%S")))

        homework_id += 1

# -------------------- Insert Test Submissions --------------------
test_submissions = [
    (1, 'The Clever Rabbit', 1, '2025-04-10 18:30:38', 0),
    (1, 'Parts of the Body', 1, '2025-04-11 13:13:31', 0),
    (6, 'My Family', 1, '2025-04-11 13:16:56', 0),
    (1, 'My Family', 1, '2025-04-11 13:24:54', 50),
    (2, 'A Day at the Park', 1, '2025-04-12 09:15:00', 40),
    (3, 'Good Habits', 1, '2025-04-12 10:20:22', 45),
    (4, 'Healthy Food', 1, '2025-04-13 11:30:12', 48),
    (5, 'Animals Around Us', 1, '2025-04-13 12:05:00', 50),
    (7, 'The Sun and the Moon', 1, '2025-04-14 14:15:18', 44),
    (8, 'The Clever Rabbit', 1, '2025-04-15 15:10:33', 47),
]
cursor.executemany('''
    INSERT INTO test_submissions (student_id, unit_title, standard, submitted_at, marks)
    VALUES (?, ?, ?, ?, ?)
''', test_submissions)

# -------------------- Insert Homework Responses --------------------
homework_responses = [
    (1, 43941057, 'Completed', 2),
    (3, 43941057, 'Completed', 2),
    (2, 30771284, 'Completed', 5),
    (4, 43941057, 'Pending', 2),
    (5, 30771284, 'Completed', 5),
    (6, 43941057, 'Completed', 2),
    (1, 30771284, 'Pending', 5),
    (3, 30771284, 'Completed', 5),
    (2, 43941057, 'Completed', 2),
    (5, 43941057, 'Reviewed', 2),
]
cursor.executemany('''
    INSERT INTO homework_responses (homework_id, student_id, status, parent_id)
    VALUES (?, ?, ?, ?)
''', homework_responses)

# Final commit and close
conn.commit()
conn.close()

print("All data successfully inserted into db.sqlite3.")
