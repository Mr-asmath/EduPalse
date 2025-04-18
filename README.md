# 📚 EduPulse: Intelligent Homework and Lesson Management System

EduPulse is a smart academic platform designed to simplify homework distribution, test submissions, and parent-student-teacher interactions in a school environment. This system is built with **Flask**, **HTML/CSS**, and **SQLite3**.

---

## 🚀 Features

- 👨‍🏫 Teacher Dashboard: Assign homework and manage class content.
- 👨‍🎓 Student Dashboard: View, complete, and submit homework/tests.
- 👨‍👩‍👧 Parent Dashboard: Monitor child homework status and performance.
- 🧑‍💼 Admin Panel: Manage users, homework, and test data.
- 📅 Test Uploads & Submissions: Track student test results with scoring.
- 🔄 Homework Completion Status: View homework progress and parent review.
- 🔐 Multi-Role Authentication System: Student, Teacher, Parent, Admin.
- 📊 Data Visualizations: Display all users, tests, and homework records.

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3
- **Database**: SQLite (`db.sqlite3`)
- **Others**: Jinja2 Templates

---

## 📂 Project Structure

```
EduPulse/
│
├── app.py                  # Main Flask application
├── db2.sqlite3             # SQLite3 database
├── templates/              # HTML templates
│   ├── home.html
│   ├── students.html
│   ├── parents.html
│   ├── teachers.html
│   ├── homeworks.html
│   ├── test_submissions.html
│   └── homework_responses.html
├── static/                 # Static files (CSS, JS)
└── README.md               # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Mr-asmath/Edupalse.git
   cd edupulse
   ```

2. **Install required dependencies**  
   ```bash
   pip install flask
   ```

3. **Run the application**  
   ```bash
   python app.py
   ```

4. **Access it in the browser**  
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📊 Sample Pages

- `/students` – Displays all student records.
- `/parents` – Displays all parent data with child linkage.
- `/teachers` – Shows registered teacher data.
- `/homeworks` – Lists all homework entries.
- `/test_submissions` – Displays submitted tests with marks.
- `/homework_responses` – Shows homework completion and review.

---

## 📌 Future Enhancements

- SMS/email notifications for parents and students.
- AI-based homework checking and suggestions.
- Export reports in PDF/Excel format.
- Admin dashboard with graphs and analytics.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

