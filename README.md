# Attendance Management System

A simple, beginner-friendly **Attendance Management System** built with **Flask**, **Bootstrap 5**, and **SQLite**. It lets you manage students and track their daily attendance through a clean, responsive web interface.

## Features

- **Dashboard** — Total students, present today, absent today, and attendance percentage at a glance.
- **Student Management** — Add, edit, delete, and view student details (Student ID, Name, Class, Email, Phone).
- **Attendance Management** — Mark students Present/Absent, view today's attendance, view/edit/delete attendance history.
- **Search & Filter** — Search students by name/ID, filter attendance by date, class, or status.
- **Automatic Database Setup** — The SQLite database and tables are created automatically on first run.
- **Secure by Design** — All SQL queries are parameterized to prevent SQL injection.
- **Responsive UI** — Built entirely with Bootstrap 5 components (navbar, cards, modals, tables, alerts).

## Tech Stack

| Layer      | Technology                     |
|------------|---------------------------------|
| Backend    | Python 3.11+, Flask             |
| Database   | SQLite (via Python's `sqlite3`) |
| Frontend   | Bootstrap 5, vanilla JavaScript |
| Templating | Jinja2 (Flask's default)        |

## Project Structure

```
final-project/
│── app.py                 # Flask routes / application logic
│── database.py             # SQLite connection + CRUD helper functions
│── requirements.txt        # Python dependencies
│── README.md                # This file
│── prompts-used.md          # AI prompts used to build this project
│── .env.example              # Example environment variables
│── attendance.db            # SQLite database (auto-created on first run)
│
├── templates/
│   ├── layout.html          # Base template (navbar, flash messages, footer)
│   ├── index.html            # Dashboard page
│   ├── students.html         # Student management page
│   └── attendance.html       # Attendance management page
│
├── static/
│   ├── css/style.css         # Custom styles
│   ├── js/script.js          # Modal population + small UX helpers
│   └── images/                # (optional) static images
│
└── screenshots/              # (optional) app screenshots for documentation
```

## Setup Instructions

### 1. Prerequisites

- Python 3.11 or newer installed
- `pip` (comes with Python)

### 2. Clone / download the project

Place the `final-project` folder wherever you'd like to work from.

### 3. Create a virtual environment (recommended)

```bash
cd final-project
python3 -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables (optional but recommended)

```bash
cp .env.example .env
# then edit .env and set a real SECRET_KEY
```

### 6. Run the application

```bash
python app.py
```

The first time it runs, `attendance.db` and its tables are created automatically — no manual setup needed.

### 7. Open in your browser

Go to: **http://127.0.0.1:5000**

## Usage Guide

1. **Add students** from the *Students* page using the "Add Student" button.
2. **Mark attendance** from the *Attendance* page — pick Present/Absent per student and click "Save".
3. **View the Dashboard** for a live summary of today's attendance.
4. **Search / filter** students by name or ID, and filter attendance history by date, class, or status.
5. **Edit or delete** any student or attendance record using the action buttons — confirmation modals prevent accidental deletes.

## Database Schema

**students**

| Column     | Type      | Notes                        |
|------------|-----------|-------------------------------|
| id         | INTEGER   | Primary key, autoincrement    |
| student_id | TEXT      | Unique, required              |
| name       | TEXT      | Required                      |
| class      | TEXT      | Required                      |
| email      | TEXT      | Optional                      |
| phone      | TEXT      | Optional                      |
| created_at | TIMESTAMP | Defaults to current time      |

**attendance**

| Column          | Type      | Notes                                    |
|-----------------|-----------|--------------------------------------------|
| id              | INTEGER   | Primary key, autoincrement                 |
| student_id      | INTEGER   | Foreign key -> students.id (cascades on delete) |
| attendance_date | TEXT      | ISO date string (YYYY-MM-DD)               |
| status          | TEXT      | "Present" or "Absent"                       |
| remarks         | TEXT      | Optional notes                              |
| created_at      | TIMESTAMP | Defaults to current time                    |

## Security Notes

- All SQL statements use parameterized queries (`?` placeholders) — user input is never concatenated into SQL strings.
- Basic server-side validation is performed on all forms (required fields, email/phone sanity checks).
- `SECRET_KEY` should always be overridden with a real random value before deploying anywhere beyond your own machine.

## Troubleshooting

- **"attendance.db already exists but looks empty/broken"** — delete `attendance.db` and restart the app; it will be recreated automatically.
- **Port already in use** — stop other running Flask apps, or run `app.run(debug=True, port=5001)` in `app.py`.
- **Changes to templates/static files not showing** — hard-refresh your browser (Ctrl/Cmd+Shift+R); make sure `FLASK_DEBUG=True` for the auto-reloader.

## License

This project is provided as an educational example and may be freely used and modified.
