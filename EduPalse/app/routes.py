import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
os.environ["USE_TF"] = "0"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
import sqlite3
from datetime import datetime
import uuid
from twilio.rest import Client
import secrets


main = Blueprint('main', __name__)
DATABASE = 'db.sqlite3'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@main.teardown_app_request
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@main.route('/')
def home():
    return render_template('welcome.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    if request.method == 'POST' or request.method == 'GET':
        # Handle JSON data (from JS fetch) or form data
        if request.is_json:

            data = request.get_json()
            id_number = data.get('id_number')
            password = data.get('password')
        else:
            id_number = request.form.get('id_number')
            password = request.form.get('password')

        # Fetch user
        cur = db.execute("SELECT * FROM users WHERE unique_id = ?", (id_number,))
        user = cur.fetchone()
        
        if user and user['password']==password:
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            session['user_name'] = user['name']

            # For JS login, return JSON response
            if request.is_json:
                return jsonify(status="success", user_type=user['user_type'])

            # For form login, redirect based on role
            if user['user_type'] == "Student":
                return redirect(url_for('main.student_home'))
            elif user['user_type'] == "Teacher":
                return redirect(url_for('main.teacher_home'))
            elif user['user_type'] == "Parent":
                return redirect(url_for('main.parent_home'))
            elif user['user_type'] == "Admin":
                return redirect(url_for('main.admin_home'))
            else:
                flash("Unknown user role.", "error")
                return redirect(url_for('main.login'))

        else:
            if request.is_json:
                return jsonify(status="fail"), 401
            

    return render_template('login.html')


@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_id = request.form.get('id')

        if not user_id:
            flash('Please enter your User ID.', 'error')
            return redirect(url_for('main.forgot_password'))

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE unique_id = ?', (user_id,)).fetchone()

        if user:
            new_password = secrets.token_urlsafe(8)
            hashed_password = new_password

            conn.execute('UPDATE users SET password = ? WHERE unique_id = ?', (hashed_password, user_id))
            conn.commit()
            conn.close()

            flash(f'Success! Your temporary password is: {new_password}', 'success')
        else:
            flash('Error: User ID not found in the system.', 'error')

        return redirect(url_for('main.forgot_password'))

    # Only renders template if GET request
    return render_template('forgot_password.html')


@main.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST' or request.method == 'GET' and request.form.get('email') is not None:

        user_type = request.form.get('user_type')
        email = request.form.get('email')
        phone = request.form.get('phone')
        unique_id = request.form.get('unique_id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('main.signup'))

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Check if email or unique_id already exists
        
       
        # Data mapping based on user_type
        name = roll_number = esim_number = student_class = section = group = attending_classes = None
        if user_type == 'Student':
            name = request.form.get('student_name')
            roll_number = request.form.get('roll_number')
            esim_number = request.form.get('esim_number')
            student_class = request.form.get('class')
            section = request.form.get('section')
            group = request.form.get('group')

        elif user_type == 'Teacher':
            name = request.form.get('teacher_name')
            attending_classes = request.form.get('attending_classes')

        elif user_type == 'Parent':
            name = request.form.get('parent_name')
            child_name = request.form.get('child_name')
            student_class = request.form.get('child_class')
            section = request.form.get('child_section')
            roll_number = None
            esim_number = None
            group = request.form.get('group')
            child_unique_id = request.form.get('child_unique_id')
            # Validate child ID exists as student
            cursor.execute("SELECT * FROM users WHERE unique_id = ? AND user_type = 'Student'", (child_unique_id,))

            if (cursor.fetchone()) == tuple:
                flash("Child's Unique ID does not exist.")
                conn.close()
                return redirect(url_for('main.login'))
            
        elif user_type == 'Admin':
            name = request.form.get('admin_name')

        else:
            flash("Invalid user type selected.")
            conn.close()
            return redirect(url_for('main.signup'))

        # Insert into DB
        

        cursor.execute("""
            INSERT INTO users (
                user_type, name, roll_number, esim_number, class, section,
                student_group, attending_classes, email, phone, unique_id, password,parent_child_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            user_type, name, roll_number, esim_number, student_class, section,
            group, attending_classes, email, phone, unique_id, password,child_unique_id
        ))
        cursor.execute("""
            UPDATE users SET parent_child_id = ? WHERE unique_id = ?;
        """, (
            unique_id,child_unique_id
        ))
        conn.commit()
        conn.close()
        flash('Account created successfully!')
        return redirect(url_for('main.login'))
        
        

    return render_template('signup.html')

    



@main.route('/dashboard')
def dashboard():
    user_type = session.get('user_type')
    user_id = session.get('user_id')
    db = get_db()
    if user_type == 'Teacher':
        lessons = db.execute("SELECT * FROM lesson WHERE teacher_id = ?", (user_id,)).fetchall()
        return render_template('dashboard.html', lessons=lessons)
    return render_template('dashboard.html')

@main.route('/assign-homework', methods=['GET', 'POST'])
def assign_homework():
    if session.get('user_type') != 'Teacher':
        flash("Unauthorized access", "error")
        return redirect(url_for('main.dashboard'))

    db = get_db()
    user_id = session.get('user_id')

    if request.method == 'POST':
        db.execute("""
            INSERT INTO homework (lesson_id, description, due_date, created_by)
            VALUES (?, ?, ?, ?)
        """, (
            request.form.get('lesson_id'),
            request.form.get('description'),
            request.form.get('due_date'),
            user_id
        ))
        db.commit()
        flash("Homework assigned successfully!", "success")
        return redirect(url_for('main.dashboard'))

    lessons = db.execute("SELECT * FROM lesson WHERE teacher_id = ?", (user_id,)).fetchall()
    return render_template('assign_homework.html', lessons=lessons)

@main.route('/student_home')
def student_home():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    db = get_db()
    user_id = session['user_id']

    # Get student's class
    cur = db.execute("SELECT class, name FROM users WHERE id = ?", (user_id,))
    student = cur.fetchone()
    if not student:
        return redirect(url_for('main.login'))

    student_class = student['class']
    student_name = student['name']

    # Fetch homework for the student's class
    homework = db.execute(
        "SELECT id, title, description, file_path, created_at FROM homework WHERE class_name = ? ORDER BY created_at DESC",
        (student_class,)
    ).fetchall()

    # Fetch tests uploaded for the student's class
    tests = db.execute(
        "SELECT id, unit_title, standard, test_date FROM uploaded_tests WHERE standard = ? ORDER BY test_date DESC",
        (student_class,)
    ).fetchall()

    # Check which tests are already completed
    available_tests = []
    for test in tests:
        test_completed = db.execute(
            "SELECT 1 FROM test_submissions WHERE student_id = ? AND unit_title = ? AND standard = ?",
            (user_id, test['unit_title'], test['standard'])
        ).fetchone()

        available_tests.append({
            'id': test['id'],
            'unit_title': test['unit_title'],
            'standard': test['standard'],
            'test_date': test['test_date'],
            'completed': bool(test_completed)
        })

    return render_template(
        'student_home.html',
        name=student_name,
        homework=homework,
        available_tests=available_tests,
        student_class = student_class
    )

@main.route('/view_homework/<int:homework_id>')
def view_homework(homework_id):
    conn = get_db()
    hw = conn.execute('SELECT * FROM homework WHERE id = ?', (homework_id,)).fetchone()
    conn.close()
    return render_template('homework_details.html', hw=hw)

@main.route('/view_homework_parents/<int:homework_id>')
def view_homework_parents(homework_id):
    conn = get_db()
    hw = conn.execute('SELECT * FROM homework WHERE id = ?', (homework_id,)).fetchone()
    conn.close()
    return render_template('homework_details_parent.html', hw=hw)


@main.route('/teacher_home')
def teacher_home():
    if 'user_type' not in session or session['user_type'] != 'Teacher':
        return redirect(url_for('main.login'))

    teacher_name = session.get('user_name')
    db = get_db()

    # Get teacher's assigned classes
    cur = db.execute("SELECT attending_classes FROM users WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    class_list = user['attending_classes'].split(",") if user and user['attending_classes'] else []

    # Get homework uploaded by this teacher
    homework_data = db.execute("""
        SELECT id, title, class_name FROM homework
        WHERE id = ?
        ORDER BY created_at DESC
    """, (session['user_id'],)).fetchall()
    class_t = db.execute("""
        SELECT attending_classes FROM users
        WHERE id = ?
    """, (session['user_id'],)).fetchall()

    return render_template('teacher_home.html',
                           teacher_name=teacher_name,
                           class_list=[cls.strip() for cls in class_list],
                           homework_data=homework_data)


@main.route('/students_details/<class_name>')
def students_details(class_name):
    db = get_db()
    
    # Fetch all students
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Student' AND class = ?", (class_name,))
    students = cur.fetchall()
    # Fetch all parents
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Parent' AND class = ?", (class_name,))
    parents = cur.fetchall()

    # Map of child_id to parent data
    parent_map = {parent['parent_child_id']: parent for parent in parents}

    # Attach parent info to each student
    student_data = []
    for student in students:
        parent = parent_map.get(student['id'])
        student_data.append({
            'student': student,
            'parent': parent
        })

    return render_template('students_details.html', student_data=student_data)


@main.route('/parent_home')
def parent_home():
    if 'user_type' not in session or session['user_type'] != 'Parent':
        return redirect(url_for('main.login'))

    db = get_db()
    parent_id = session.get('user_id')

    # Get parent details
    parent = db.execute(
        "SELECT id, name, class, unique_id, parent_child_id FROM users WHERE id = ?", 
        (parent_id,)
    ).fetchone()

    if not parent:
        return "Parent information not found."

    # Get child details using parent's unique_id stored in parent_child_id
    child_tb = db.execute(
        "SELECT id, name, class, unique_id FROM users WHERE unique_id = ?", 
        (parent['parent_child_id'],)
    ).fetchone()

    if not child_tb:
        return "Linked child not found. Please check the parent-child ID relationship."

    child_id = child_tb['unique_id']  # Still using unique_id to check in homework_responses
    child_db_id = child_tb['id']      # Actual `id` used for test_submissions if needed
    child_name = child_tb['name']
    child_class = child_tb['class']

    # Get homework for child class, and mark completion using unique_id
    # Fetch homework list (without JOIN)
    hw_query = '''
        SELECT 
            hw.id AS hw_id,
            hw.title,
            hw.description
        FROM homework hw
        WHERE hw.class_name = ?
    '''
    rows = db.execute(hw_query, (child_class,)).fetchall()

    # Fetch status from homework_responses separately
    rows2 = db.execute("SELECT homework_id, status FROM homework_responses WHERE student_id = ?", (child_db_id,)).fetchall()

    # Pass both datasets to the template
    return render_template('parent_home.html',
                        parent_name=parent['name'],
                        child_name=child_name,
                        child_class=child_class,
                        homework_list=rows,
                        response_statuses=rows2)





@main.route('/mark_homework_complete/<int:homework_id>', methods=['POST'])
def mark_homework_complete(homework_id):
    if 'user_type' not in session or session['user_type'] != 'Parent':
        return redirect(url_for('main.login'))

    db = get_db()
    parent_id = session['user_id']

    # Get parent's child unique_id
    parent = db.execute("SELECT parent_child_id FROM users WHERE id = ?", (parent_id,)).fetchone()
    if not parent or not parent['parent_child_id']:
        return "Parent-child link not found."

    # Get the child's actual ID using the unique_id from parent_child_id
    child = db.execute("SELECT id FROM users WHERE unique_id = ?", (parent['parent_child_id'],)).fetchone()
    if not child:
        return "Child not found."



    # Insert the response into the homework_responses table
    db.execute("""
        INSERT INTO homework_responses (homework_id, student_id, parent_id, status)
        VALUES (?, ?, ?, ?)""",
        (homework_id, child['id'], parent_id, 'Completed')
    )
    db.commit()

    return redirect(url_for('main.parent_home'))


@main.route('/view_homework_responses/<int:homework_id>')
def view_homework_responses(homework_id):
    db = get_db()
    homework = db.execute("SELECT title, class_name FROM homework WHERE id = ?", (homework_id,)).fetchone()
    hr = db.execute("SELECT status FROM homework_responses").fetchone()
    students = db.execute("""
    SELECT 
        u.name, 
        u.roll_number,
        hr.status
    FROM users u
    LEFT JOIN homework_responses hr 
        ON u.id = hr.student_id AND hr.homework_id = ?
    WHERE u.class = ? AND u.user_type = 'Student'
""", (homework_id, homework['class_name'])).fetchall()
    processed_students = []
    for student in students:
        status = hr['status']

        if status is None:
            status = 'Completed'
        elif status == 'Pending':
            status = 'Pending'
        processed_students.append({
            'name': student['name'],
            'roll_number': student['roll_number'],
            'status': status
        })

    return render_template('homework_responses.html',
                           students=processed_students,
                           homework_title=homework['title'])


@main.route('/admin_home')
def admin_home():
    db = get_db()
    # Get teachers
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Teacher'")
    teachers = cur.fetchall()

    # Get students with their parent details
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Student'")
    students = cur.fetchall()

    cur = db.execute("SELECT * FROM users WHERE user_type = 'Parent'")
    parents = cur.fetchall()
    parents_dict = {parent[13]: parent for parent in parents}  # key: student_id

    # Get all unique class names for homework
    cur = db.execute("SELECT DISTINCT class_name FROM homework")
    homework_classes = cur.fetchall()

    # Get all unique standards for tests
    cur = db.execute("SELECT DISTINCT standard FROM uploaded_tests  ")
    test_classes = cur.fetchall()

    return render_template('admin_home.html',
                           teachers=teachers,
                           students=students,
                           parents=parents_dict,
                           homework_classes=homework_classes,
                           test_classes=test_classes)

@main.route('/admin/teacher_analysis')
def teacher_analysis():
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Teacher'")
    teachers = cur.fetchall()  # Assuming teachers is a list of Row objects (dict-like)
    return render_template('admin_teacher_analysis.html', teachers=teachers)

# --- UPDATE TEACHER ROUTE ---
@main.route('/admin/update_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher(teacher_id):
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        attending_classes = request.form['attending_classes']

        cur = db.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, attending_classes = ? WHERE id = ? AND user_type = 'Teacher'",
            (name, email, phone, attending_classes, teacher_id)
        )
        db.commit()
        flash("Teacher updated successfully!")
        return redirect(url_for('main.teacher_analysis'))

    # GET method
    cur = db.execute("SELECT * FROM users WHERE id = ? AND user_type = 'Teacher'", (teacher_id,))
    teacher = cur.fetchone()

    if teacher is None:
        flash("Teacher not found.")
        return redirect(url_for('main.teacher_analysis'))

    return render_template('update_teacher.html', teacher=teacher)


# --- DELETE TEACHER ROUTE ---
@main.route('/admin/delete_teacher/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    db = get_db()
    cur = db.execute("DELETE FROM users WHERE id = ? AND user_type = 'Teacher'", (teacher_id,))
    db.commit()
    flash("Teacher deleted successfully.")
    return redirect(url_for('main.teacher_analysis'))

@main.route('/admin/student_details')
def student_details():
    db = get_db()
    
    # Fetch all students
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Student'")
    students = cur.fetchall()

    # Fetch all parents
    cur = db.execute("SELECT * FROM users WHERE user_type = 'Parent'")
    parents = cur.fetchall()

    # Map of child_id to parent data
    parent_map = {parent['parent_child_id']: parent for parent in parents}

    # Attach parent info to each student
    student_data = []
    for student in students:
        parent = parent_map.get(student['id'])
        student_data.append({
            'student': student,
            'parent': parent
        })

    return render_template('student_details.html', student_data=student_data)

@main.route('/admin/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        roll_number = request.form['roll_number']
        esim_number = request.form['esim_number']
        class_name = request.form['class']
        section = request.form['section']

        cur = db.execute("""
            UPDATE users 
            SET name = ?, email = ?, phone = ?, roll_number = ?, esim_number = ?, class = ?, section = ?
            WHERE id = ? AND user_type = 'Student'
        """, (name, email, phone, roll_number, esim_number, class_name, section, student_id))
        db.commit()
        flash("Student information updated successfully!", "success")
        return redirect(url_for('main.student_details'))

    # GET request
    cur = db.execute("SELECT * FROM users WHERE id = ? AND user_type = 'Student'", (student_id,))
    student = cur.fetchone()

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('main.student_details'))

    return render_template('update_student.html', student=student)


# DELETE student
@main.route('/admin/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    db = get_db()
    cur = db.execute("DELETE FROM users WHERE id = ? AND user_type = 'Student'", (student_id,))
    db.commit()
    flash("Student deleted successfully!", "warning")
    return redirect(url_for('main.student_details'))




@main.route('/admin/class_homeworks')
def homework_classes():
    db = get_db()

    # Fetch distinct class names that have homework
    cur = db.execute("""
        SELECT DISTINCT class_name 
        FROM homework 
        ORDER BY class_name
    """)
    classes = cur.fetchall()

    return render_template('admin_class_homeworks.html', classes=classes)

@main.route('/admin/class_homeworks/<class_name>')
def class_homeworks(class_name):
    db = get_db()

    # Get homework and corresponding teacher name
    cur = db.execute("""
        SELECT h.*, u.name as teacher_name
        FROM homework h
        JOIN users u ON h.teacher_id = u.id
        WHERE h.class_name = ?
        ORDER BY h.created_at DESC
    """, (class_name,))
    homeworks = cur.fetchall()
    return render_template('admin_homeworks_class.html', class_name=class_name, homeworks=homeworks)

@main.route('/admin/update_homework/<int:homework_id>', methods=['GET', 'POST'])
def update_homework(homework_id):
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        db.execute("UPDATE homework SET title = ?, description = ? WHERE id = ?", (title, description, homework_id))
        db.commit()
        return redirect(url_for('main.homework_classes'))

    cur = db.execute("SELECT * FROM homework WHERE id = ?", (homework_id,))
    homework = cur.fetchone()
    return render_template('admin_update_homework.html', homework=homework)

@main.route('/admin/delete_homework/<int:homework_id>', methods=['POST'])
def delete_homework(homework_id):
    db = get_db()
    db.execute("DELETE FROM homework WHERE id = ?", (homework_id,))
    db.commit()
    return redirect(url_for('main.class_homeworks'))


@main.route('/admin/test_classes')
def test_classes():
    db = get_db()

    # Get distinct classes from uploaded tests
    cur = db.execute("SELECT DISTINCT standard FROM uploaded_tests ORDER BY standard")
    classes = cur.fetchall()
    return render_template('admin_class_tests.html', classes=classes)


@main.route('/admin/tests_classes/<class_name>')
def tests_classes(class_name):
    db = get_db()

    # Get all tests for the class
    cur = db.execute("""
        SELECT t.*, u.name AS teacher_name
        FROM uploaded_tests t
        LEFT JOIN homework h ON h.class_name = t.standard
        LEFT JOIN users u ON h.teacher_id = u.id
        WHERE t.standard = ?
        GROUP BY t.id
        ORDER BY t.test_date DESC
    """, (class_name,))
    tests = cur.fetchall()

    # Get all student submissions for the class
    cur = db.execute("""
        SELECT ts.*, u.name AS student_name
        FROM test_submissions ts
        JOIN users u ON ts.student_id = u.id
        WHERE ts.standard = ?
    """, (class_name,))
    submissions = cur.fetchall()

    cur = db.execute("""
        SELECT name
        FROM users where user_type = 'Teacher' 
    """)
    teachers = cur.fetchall()

    cur = db.execute("""
        SELECT id,marks
        FROM test_submissions
    """) 
    mark_total =0
    sno =0
    mark_s = cur.fetchall()
    for mark_ss in mark_s:
        mark_total +=mark_ss['marks']
        sno+=1
    average_marks = mark_total/sno
    average_marks = round(average_marks,2)
    submission_rate = mark_ss['id']
    return render_template('admin_class_tests_view.html', class_name=class_name, tests=tests, submissions=submissions, teachers=teachers, average_marks=average_marks,submission_rate=submission_rate)



UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'png', 'jpeg'} 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload_homework/<class_name>', methods=['GET', 'POST'])
def upload_homework(class_name):
    # Check if user is logged in and is a teacher
    if 'user_type' not in session or session['user_type'] != 'Teacher':
        return redirect(url_for('main.login'))

    if request.method == 'GET':
        # Show the homework upload form
        return render_template('upload_homework.html', class_name=class_name)

    # POST method: handle homework upload
    title = request.form.get('title')
    description = request.form.get('description')
    file = request.files.get('file')

    # Handle file upload (check if file exists and is allowed)
    file_path = None
    if file and file.filename != '':
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            flash("Invalid file format. Allowed formats are: pdf, docx, txt, jpg, png, jpeg.", "danger")
            return render_template('upload_homework.html', class_name=class_name, error="Invalid file format")

    # Insert homework data into the database
    db = get_db()
    db.execute("""
        INSERT INTO homework (teacher_id, class_name, title, description, file_path)
        VALUES (?, ?, ?, ?, ?)
    """, (session['user_id'], class_name, title, description, file_path))
    db.commit()

    # --- WhatsApp Notification Part ---
    try:
        students = db.execute(
            "SELECT name, phone FROM users WHERE role = 'Student' AND class = ?",
            (class_name,)
        ).fetchall()

        if students:
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            from_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

            for student in students:
                message_body = f"📘 Hi {student['name']}, new homework has been uploaded for Class {class_name}:\n\n📌 *{title}*\n📝 {description}"
                to_whatsapp = f"whatsapp:{student['phone']}"
                client.messages.create(
                    body=message_body,
                    from_=from_whatsapp_number,
                    to=to_whatsapp
                )
    except Exception as e:
        flash(f"Homework uploaded, but WhatsApp messages failed: {e}", "warning")

    
    return redirect(url_for('main.teacher_home', class_name=class_name))

@main.route('/class_homeworks/<class_name>')
def view_class_homeworks(class_name):
    if 'user_type' not in session or session['user_type'] != 'Teacher':
        return redirect(url_for('main.login'))

    db = get_db()
    homeworks = db.execute("""
        SELECT id, title, description, created_at
        FROM homework
        WHERE class_name = ? AND teacher_id = ?
        ORDER BY created_at DESC
    """, (class_name, session['user_id'])).fetchall()

    return render_template('class_homeworks.html', class_name=class_name, homeworks=homeworks)

lesson_dataset = pd.read_csv("standard_dataset.csv")

@main.route('/upload_dataset', methods=['GET', 'POST'])
def upload_dataset():
    db = get_db()
    class_list = request.args.get('standard')

    if class_list is not None:
        class_list = int(class_list)
    if request.method == 'POST':
        
        standard = request.form.get('standard')
        
        unit_title = request.form.get('unit')
        test_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            df = pd.read_csv("standard_dataset.csv")

            global lesson_dataset
            lesson_dataset = df  # Store in memory or update your system-wide logic

            # Insert metadata into uploaded_tests table
            db.execute(
                "INSERT INTO uploaded_tests (standard, unit_title, test_date) VALUES (?, ?, ?)",
                (standard, unit_title, test_date)
            )
            db.commit()

            flash('Dataset uploaded and test registered successfully!', 'success')
            return redirect(url_for('main.teacher_home'))
        except Exception as e:
            flash(f'Failed to read dataset: {str(e)}', 'danger')
    
    standards = sorted(lesson_dataset[lesson_dataset['standard'] == class_list]['standard'].unique()) if lesson_dataset is not None else []
    unit_titles = sorted(lesson_dataset[lesson_dataset['standard'] == class_list]['unit_title'].unique()) if lesson_dataset is not None else []


    return render_template('upload_dataset.html', standards=standards, unit_titles=unit_titles)


@main.route('/available_tests')
def available_tests():
    db = get_db()
    student_id = session.get('user_id')

    student = db.execute("SELECT * FROM users WHERE id = ?", (student_id,)).fetchone()
    standard = student['standard']

    tests = db.execute(
        "SELECT * FROM uploaded_tests WHERE standard = ?",
        (standard,)
    ).fetchall()

    return render_template('available_tests.html', tests=tests)


@main.route('/view_lessons/<int:standard>')
def view_lessons_and_generate_test(standard):

    if lesson_dataset is None:
        flash("No dataset loaded. Please upload first.", "warning")
        return redirect(url_for('main.upload_dataset'))

    try:
        lessons = lesson_dataset[lesson_dataset['standard'] == standard]
        if lessons.empty:
            flash(f"No lessons found for standard {standard}.", "info")
        return render_template(
            'lesson_test_page.html',
            standard=standard,
            lessons=lessons.to_dict(orient='records')
        )
    except Exception as e:
        flash(f"Error loading lessons: {str(e)}", "danger")
        return redirect(url_for('main.generate_test'))
    
@main.route('/select_standard')
def select_standard():

    if lesson_dataset is None:
        flash("Dataset not loaded.", "warning")
        return redirect(url_for('main.upload_dataset'))

    standards = sorted(lesson_dataset['standard'].unique())
    return render_template('select_standard.html', standards=standards)


@main.route('/student_unit_questions/<int:standard>/<unit_title>', methods=['GET', 'POST'])
def student_unit_questions(standard, unit_title):
    db = get_db()
    user_id = session.get('user_id')

    # Check if student is logged in
    if not user_id:
        return redirect(url_for('main.login'))

    # Check if test already completed
    completed = db.execute(
        "SELECT 1 FROM test_submissions WHERE student_id = ? AND unit_title = ? AND standard = ?",
        (user_id, unit_title, standard)
    ).fetchone()

    if completed:
        flash("You have already completed this test.", "info")
        return redirect(url_for('main.student_home'))

    # Load the CSV file with questions (standard_dataset.csv)
    try:
        dataset = pd.read_csv("standard_dataset.csv")
    except Exception as e:
        flash(f"Error loading questions dataset: {e}", "danger")
        return redirect(url_for('main.student_home'))

    # Filter questions for the correct standard and unit
    questions = dataset[
        (dataset['standard'] == standard) & 
        (dataset['unit_title'] == unit_title)
    ]

    if questions.empty:
        flash("No questions found for this unit.", "info")
        return redirect(url_for('main.student_home'))

    if request.method == 'POST':
        total_questions = len(questions)
        correct_count = 0

        for i, row in questions.reset_index().iterrows():
            student_answer_1 = request.form.get(f"answer_{i+1}_1", "").strip().lower()
            student_answer_2 = request.form.get(f"answer_{i+1}_2", "").strip().lower()
            student_answer_3 = request.form.get(f"answer_{i+1}_3", "").strip().lower()
            student_answer_4 = request.form.get(f"answer_{i+1}_4", "").strip().lower()
            student_answer_5 = request.form.get(f"answer_{i+1}_5", "").strip().lower()

            correct_answer_1 = str(row['sample_answer_1']).strip().lower()
            correct_answer_2 = str(row['sample_answer_2']).strip().lower()
            correct_answer_3 = str(row['sample_answer_3']).strip().lower()
            correct_answer_4 = str(row['sample_answer_4']).strip().lower()
            correct_answer_5 = str(row['sample_answer_5']).strip().lower()


            # Compare answers
            if student_answer_1 == correct_answer_1:
                correct_count += 1
            if student_answer_2 == correct_answer_2:
                correct_count += 1
            if student_answer_3 == correct_answer_3:
                correct_count += 1
            if student_answer_4 == correct_answer_4:
                correct_count += 1
            if student_answer_5 == correct_answer_5:
                correct_count += 1

        total_possible = total_questions * 2
        marks_obtained = int((correct_count / total_possible) * 100)

        db.execute(
            "INSERT INTO test_submissions (student_id, unit_title, standard, submitted_at, marks) VALUES (?, ?, ?, datetime('now'), ?)",
            (user_id, unit_title, standard, marks_obtained)
        )
        db.commit()
        flash(f"Test submitted successfully! Your score: {marks_obtained}%", "success")
        return redirect(url_for('main.student_home'))

    return render_template('student_questions.html', questions=questions.to_dict(orient='records'))


@main.route('/view_test_marks', methods=['GET'])
def view_test_marks():
    unit_title = request.args.get('unit_title')
    if not unit_title:
        flash("Unit title not provided", "warning")
        return redirect(url_for('main.teacher_home'))

    db = get_db()
    results = db.execute("""
        SELECT 
            ts.id,
            u.name AS student_name,
            ts.unit_title,
            ts.standard,
            ts.submitted_at,
            COALESCE(ts.marks, 'Not Marked') AS marks
        FROM test_submissions ts
        JOIN users u ON ts.student_id = u.id
        WHERE ts.unit_title = ?
        ORDER BY ts.submitted_at DESC
    """, (unit_title,)).fetchall()

    return render_template("view_test_marks.html", unit_title=unit_title, results=results)

@main.route('/view_child_marks')
def view_child_marks():
    if 'user_type' not in session or session['user_type'] != 'Parent':
        return redirect(url_for('main.login'))

    db = get_db()
    parent_id = session.get('user_id')

    # Get child's unique_id from parent
    parent = db.execute("SELECT name, unique_id FROM users WHERE id = ?", (parent_id,)).fetchone()
    if not parent:
        return "Parent not found."

    # Get child's actual ID from users table using the unique_id
    child = db.execute("SELECT parent_child_id FROM users WHERE unique_id = ?", (parent['unique_id'],)).fetchone()
    child = db.execute("SELECT id,name FROM users WHERE unique_id = ?", (child['parent_child_id'],)).fetchone()
    if not child:
        return "Child not found."

    child_id = child['id']

    # Now fetch test submissions only for that child
    marks_query = '''
        SELECT 
            ts.id,
            u.name AS student_name,
            ts.unit_title,
            ts.standard,
            ts.submitted_at,
            COALESCE(ts.marks, 'Not Marked') AS marks
        FROM test_submissions ts
        JOIN users u ON ts.student_id = u.id
        WHERE ts.student_id = ?
        ORDER BY ts.submitted_at DESC
    '''
    test_marks = db.execute(marks_query, (child_id,)).fetchall()

    return render_template('child_marks.html',
                           child_name=child['name'],
                           test_marks=test_marks)
