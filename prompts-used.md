# Prompts Used

This file documents the prompt(s) used to generate this project with an AI assistant (Claude), as commonly required for coursework / bootcamp submissions.

## Primary Prompt

> Act as an expert Python developer and technical instructor. Build a simple, beginner-friendly Attendance Management System using Python, Flask, Bootstrap 5, and SQLite.
>
> Requirements:
> - Use Python 3.11+
> - Use Flask as the backend framework
> - Use Bootstrap 5 for a modern, responsive user interface
> - Use SQLite with Python's built-in sqlite3 module
> - Use parameterized SQL queries to prevent SQL injection
> - Write clean, modular, and well-commented code suitable for beginners
>
> Features requested:
> - Dashboard with Total Students, Present Today, Absent Today, Attendance Percentage
> - Student Management (Add / Edit / Delete / View)
> - Attendance Management (Mark Present/Absent, view today's attendance, view history, edit/delete records)
> - Search & Filter (by name/ID, date, class, status)
> - Automatic SQLite database creation with `students` and `attendance` tables
> - Backend with CRUD operations, dashboard statistics, form validation, error handling (try/except), and flash messages
> - UI built entirely with Bootstrap 5 components: responsive navbar, dashboard cards, forms, tables, search bar, filter dropdowns, edit modal, delete confirmation modal, alerts, footer
> - Specific project folder structure (app.py, database.py, templates/, static/, requirements.txt, README.md, prompts-used.md, .env.example)

## Follow-up considerations applied while generating the project

- Kept all database logic isolated in `database.py` (separation of concerns) so `app.py` only handles HTTP routing/validation.
- Used `sqlite3.Row` + parameterized queries (`?` placeholders) everywhere - no string-formatted SQL.
- Implemented "View Student Details" as a Bootstrap modal populated via `data-*` attributes and JS, rather than a separate page, to keep the UI simple and fast for beginners.
- Added a small amount of server-side form validation (required fields, basic email/phone sanity checks) with `flash()` messages for feedback.
- Used `ON DELETE CASCADE` on the `attendance.student_id` foreign key so deleting a student cleans up their attendance history automatically.
- Prevented duplicate attendance rows for the same student/date by updating the existing record instead of inserting a new one.

## Tools

- AI Assistant: Claude (Anthropic)
- Manual review: code was reviewed for correctness, security (parameterized queries), and readability before delivery.
