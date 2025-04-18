from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def fetch_data(query):
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    return render_template('view_home.html')

@app.route('/students')
def students():
    data = fetch_data("SELECT * FROM users WHERE user_type = 'Student'")
    return render_template('students.html', data=data)

@app.route('/parents')
def parents():
    data = fetch_data("SELECT * FROM users WHERE user_type = 'Parent'")
    return render_template('parents.html', data=data)

@app.route('/teachers')
def teachers():
    data = fetch_data("SELECT * FROM users WHERE user_type = 'Teacher'")
    return render_template('teachers.html', data=data)

@app.route('/homeworks')
def homeworks():
    data = fetch_data("SELECT * FROM homework")
    return render_template('homeworks.html', data=data)

@app.route('/test_submissions')
def test_submissions():
    data = fetch_data("SELECT * FROM test_submissions")
    return render_template('test_submissions.html', data=data)

@app.route('/homework_responses')
def homework_responses():
    data = fetch_data("SELECT * FROM homework_responses")
    return render_template('homework_responses.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
