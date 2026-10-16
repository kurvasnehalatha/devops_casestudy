# Student Management System

A beginner-friendly Flask web application for managing student records with SQLite and SQLAlchemy.

## Features

- Dashboard with total students and recently added students
- Add, view, edit, and delete student records
- Search by student ID, name, or email
- Filter by department and course
- Student detail page with academic records
- Add grades and academic year information
- Duplicate validation for student IDs and email addresses
- Bootstrap 5 responsive UI
- Flash notifications for success and error messages
- CSRF protection and server-side validation

## Project Structure

```text
student-management-system/
├── app.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       ├── 404.html
│       ├── 500.html
│       ├── base.html
│       ├── dashboard.html
│       ├── student_detail.html
│       ├── student_form.html
│       └── students.html
├── .env.example
├── requirements.txt
├── README.md
└── student_management.db
```

## Windows PowerShell Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:FLASK_SECRET_KEY = "your-secret-key"
$env:DATABASE_URL = "sqlite:///student_management.db"
```

## Run the Application

```powershell
python app.py
```

Then open the app in your browser:

```text
http://127.0.0.1:5000
```

## Notes

- The database is initialized without deleting existing records.
- Default departments and courses are seeded only when the database is empty.
- The app reads configuration values from environment variables. Copy `.env.example` to `.env` if you want a local environment file.
- This project intentionally keeps the implementation simple and beginner-friendly.
