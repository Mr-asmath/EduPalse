import sqlite3

# Connect to the existing database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
"""
# New data to check for duplicates
new_data_to_check = [
    {'email': 'eliparent2@gmail.com', 'unique_id': '47920131'},
    {'email': 'felixparent2@gmail.com', 'unique_id': '47920132'},
    {'email': 'gavinparent2@gmail.com', 'unique_id': '47920133'},
    {'email': 'harveyparent2@gmail.com', 'unique_id': '47920134'},
    {'email': 'isaacparent2@gmail.com', 'unique_id': '47920135'},
    {'email': 'jasperparent2@gmail.com', 'unique_id': '47920136'},
    {'email': 'kadenparent2@gmail.com', 'unique_id': '47920137'},
    {'email': 'loganparent2@gmail.com', 'unique_id': '47920138'},
    {'email': 'milesparent2@gmail.com', 'unique_id': '47920139'},
    {'email': 'noelparent2@gmail.com', 'unique_id': '47920140'}
]



INSERT INTO users (user_type, name, roll_number, esim_number, class, section, student_group, attending_classes, email, phone, unique_id, password, parent_child_id) VALUES ('Parent', 'Eli', NULL, NULL, NULL, NULL, NULL, NULL, 'eliparent2@gmail.com', '9876543031', '85920131', 'Parent@104', '65920131'), ('Parent', 'Felix', NULL, NULL, NULL, NULL, NULL, NULL, 'felixparent2@gmail.com', '9876543032', '85920132', 'Parent@104', '65920132'), ('Parent', 'Gavin', NULL, NULL, NULL, NULL, NULL, NULL, 'gavinparent2@gmail.com', '9876543033', '85920133', 'Parent@104', '65920133'), ('Parent', 'Harvey', NULL, NULL, NULL, NULL, NULL, NULL, 'harveyparent2@gmail.com', '9876543034', '85920134', 'Parent@104', '65920134'), ('Parent', 'Isaac', NULL, NULL, NULL, NULL, NULL, NULL, 'isaacparent2@gmail.com', '9876543035', '85920135', 'Parent@104', '65920135'), ('Parent', 'Jasper', NULL, NULL, NULL, NULL, NULL, NULL, 'jasperparent2@gmail.com', '9876543036', '85920136', 'Parent@104', '65920136'), ('Parent', 'Kaden', NULL, NULL, NULL, NULL, NULL, NULL, 'kadenparent2@gmail.com', '9876543037', '85920137', 'Parent@104', '65920137'), ('Parent', 'Logan', NULL, NULL, NULL, NULL, NULL, NULL, 'loganparent2@gmail.com', '9876543038', '85920138', 'Parent@104', '65920138'), ('Parent', 'Miles', NULL, NULL, NULL, NULL, NULL, NULL, 'milesparent2@gmail.com', '9876543039', '85920139', 'Parent@104', '65920139'), ('Parent', 'Noel', NULL, NULL, NULL, NULL, NULL, NULL, 'noelparent2@gmail.com', '9876543040', '85920140', 'Parent@104', '65920140');


#DELETE FROM users WHERE user_type = 'Student' AND class = 4 AND id NOT IN (SELECT MIN(id) FROM users WHERE user_type = 'Student' AND class = 4 GROUP BY name);


# Check for existence in the database
for entry in new_data_to_check:
    email = entry['email']
    unique_id = entry['unique_id']

    # Check if the email already exists
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    email_exists = cursor.fetchone() is not None

    # Check if the unique_id already exists
    cursor.execute("SELECT 1 FROM users WHERE unique_id = ?", (unique_id,))
    id_exists = cursor.fetchone() is not None

    # Output the result
    print(f"Email: {email} - {'✅ Exists' if email_exists else '❌ Not found'}")
    print(f"Unique ID: {unique_id} - {'✅ Exists' if id_exists else '❌ Not found'}")
    print('-' * 40)

# Close the connection
conn.close()
"""

# List of parent_child_id values (from your given data)
parent_child_ids = [
    43941057, 30771284, 51128869, 59694369, 79854560, 30870211, 30870212,
    30870213, 30870214, 30870215, 30870216, 30870217, 30870218, 30870219,
    30870220, 30870321, 30870322, 30870323, 30870324, 30870325, 30870326,
    30870327, 30870328, 30870329, 30870330, 30870111, 30870101, 30870102,
    30870103, 30870104, 30870105, 30870106, 30870107, 30870108, 30870109,
    30870110, 47920131, 47920132, 47920133, 47920134, 47920135, 47920136,
    47920137, 47920138, 47920139, 47920140, 85920131, 85920132, 85920133,
    85920134, 85920135, 85920136, 85920137, 85920138, 85920139, 85920140
]

# Check if parent_child_id exists in unique_id
for parent_child_id in parent_child_ids:
    cursor.execute("""
        SELECT * FROM users WHERE unique_id  = ?
    """, (parent_child_id,))
    
    result = cursor.fetchall()

    if not result:
        print(f"No match found for parent_child_id: {parent_child_id}")
    else:
        print(f"Found match for parent_child_id: {parent_child_id}")
        for row in result:
            print(row)

# Close the database connection
conn.close()
