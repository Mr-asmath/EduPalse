from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10), nullable=False)  # 'Student' or 'Teacher'
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50))
    esim_number = db.Column(db.String(50))
    class_name = db.Column(db.String(10))
    section = db.Column(db.String(10))
    group_name = db.Column(db.String(50))
    attending_classes = db.Column(db.String(100))
    print(attending_classes)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Add relationship backrefs if needed
    lessons = db.relationship('Lesson', backref='teacher', lazy=True, foreign_keys='Lesson.teacher_id')
    created_homeworks = db.relationship('Homework', backref='creator', lazy=True, foreign_keys='Homework.created_by')
    submissions = db.relationship('Submission', backref='student', lazy=True, foreign_keys='Submission.student_id')

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    homeworks = db.relationship('Homework', backref='lesson', lazy=True)

class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    submissions = db.relationship('Submission', backref='homework', lazy=True)

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime)
