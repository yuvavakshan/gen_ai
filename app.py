"""
app.py
------
Main Flask application for the Attendance Management System.

Routes are grouped into three areas:
    1. Dashboard            (/)
    2. Student management   (/students ...)
    3. Attendance management (/attendance ...)

All database work is delegated to database.py - this file focuses on
handling HTTP requests, validating input, and rendering templates.
"""

import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

import database as db

# Load environment variables from .env (if present)
load_dotenv()

app = Flask(__name__)
# SECRET_KEY is required for flash messages to work. In production this
# should be set via an environment variable (see .env.example).
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def is_valid_email(email):
    """Very small, beginner-friendly email sanity check (not a full RFC validator)."""
    if not email:
        return True  # email is optional
    return "@" in email and "." in email.split("@")[-1]


def validate_student_form(form):
    """
    Validate the Add/Edit Student form.
    Returns a list of error strings (empty list = valid).
    """
    errors = []

    if not form.get("student_id", "").strip():
        errors.append("Student ID is required.")
    if not form.get("name", "").strip():
        errors.append("Full name is required.")
    if not form.get("class", "").strip():
        errors.append("Class is required.")
    if not is_valid_email(form.get("email", "").strip()):
        errors.append("Please enter a valid email address.")

    phone = form.get("phone", "").strip()
    if phone and not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
        errors.append("Phone number should contain digits only.")

    return errors


# ---------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------

@app.route("/")
def index():
    """Home page: shows summary statistics for the dashboard cards."""
    try:
        stats = db.get_dashboard_stats()
    except Exception as e:
        flash(f"Could not load dashboard statistics: {e}", "danger")
        stats = {"total_students": 0, "present_today": 0, "absent_today": 0, "attendance_percentage": 0}

    return render_template("index.html", stats=stats, today=date.today().isoformat())


# ---------------------------------------------------------------------
# STUDENT MANAGEMENT
# ---------------------------------------------------------------------

@app.route("/students")
def students():
    """List all students, with optional search and class filter."""
    search_query = request.args.get("q", "").strip()
    class_filter = request.args.get("class_filter", "").strip()

    try:
        student_list = db.get_all_students(search_query or None, class_filter or None)
        classes = db.get_distinct_classes()
    except Exception as e:
        flash(f"Error loading students: {e}", "danger")
        student_list, classes = [], []

    return render_template(
        "students.html",
        students=student_list,
        classes=classes,
        search_query=search_query,
        class_filter=class_filter,
    )


@app.route("/students/add", methods=["POST"])
def add_student():
    """Handle submission of the 'Add Student' form."""
    errors = validate_student_form(request.form)
    if errors:
        for err in errors:
            flash(err, "danger")
        return redirect(url_for("students"))

    success, message = db.add_student(
        request.form["student_id"].strip(),
        request.form["name"].strip(),
        request.form["class"].strip(),
        request.form.get("email", "").strip(),
        request.form.get("phone", "").strip(),
    )
    flash(message, "success" if success else "danger")
    return redirect(url_for("students"))


@app.route("/students/edit/<int:pk>", methods=["POST"])
def edit_student(pk):
    """Handle submission of the 'Edit Student' modal form."""
    errors = validate_student_form(request.form)
    if errors:
        for err in errors:
            flash(err, "danger")
        return redirect(url_for("students"))

    success, message = db.update_student(
        pk,
        request.form["student_id"].strip(),
        request.form["name"].strip(),
        request.form["class"].strip(),
        request.form.get("email", "").strip(),
        request.form.get("phone", "").strip(),
    )
    flash(message, "success" if success else "danger")
    return redirect(url_for("students"))


@app.route("/students/delete/<int:pk>", methods=["POST"])
def delete_student(pk):
    """Handle deletion of a student (triggered from the confirmation modal)."""
    success, message = db.delete_student(pk)
    flash(message, "success" if success else "danger")
    return redirect(url_for("students"))


# ---------------------------------------------------------------------
# ATTENDANCE MANAGEMENT
# ---------------------------------------------------------------------

@app.route("/attendance")
def attendance():
    """
    Attendance page: lets users mark today's attendance and view/filter
    attendance history.
    """
    date_filter = request.args.get("date_filter", "").strip()
    class_filter = request.args.get("class_filter", "").strip()
    status_filter = request.args.get("status_filter", "").strip()

    try:
        all_students = db.get_all_students()
        classes = db.get_distinct_classes()
        todays_status = db.get_todays_attendance_for_students()
        records = db.get_attendance_records(
            date_filter or None, class_filter or None, status_filter or None
        )
    except Exception as e:
        flash(f"Error loading attendance data: {e}", "danger")
        all_students, classes, todays_status, records = [], [], {}, []

    return render_template(
        "attendance.html",
        students=all_students,
        classes=classes,
        todays_status=todays_status,
        records=records,
        today=date.today().isoformat(),
        date_filter=date_filter,
        class_filter=class_filter,
        status_filter=status_filter,
    )


@app.route("/attendance/mark", methods=["POST"])
def mark_attendance():
    """
    Mark a single student Present/Absent for a given date.
    (Called once per student row on the attendance page.)
    """
    try:
        student_pk = int(request.form["student_pk"])
    except (KeyError, ValueError):
        flash("Invalid student selected.", "danger")
        return redirect(url_for("attendance"))

    attendance_date = request.form.get("attendance_date", "").strip() or date.today().isoformat()
    status = request.form.get("status", "").strip()
    remarks = request.form.get("remarks", "").strip()

    if status not in ("Present", "Absent"):
        flash("Status must be Present or Absent.", "danger")
        return redirect(url_for("attendance"))

    success, message = db.mark_attendance(student_pk, attendance_date, status, remarks)
    flash(message, "success" if success else "danger")
    return redirect(url_for("attendance"))


@app.route("/attendance/edit/<int:pk>", methods=["POST"])
def edit_attendance(pk):
    """Edit an existing attendance record (status/remarks) via the edit modal."""
    status = request.form.get("status", "").strip()
    remarks = request.form.get("remarks", "").strip()

    if status not in ("Present", "Absent"):
        flash("Status must be Present or Absent.", "danger")
        return redirect(url_for("attendance"))

    success, message = db.update_attendance(pk, status, remarks)
    flash(message, "success" if success else "danger")
    return redirect(url_for("attendance"))


@app.route("/attendance/delete/<int:pk>", methods=["POST"])
def delete_attendance(pk):
    """Delete an attendance record (triggered from the confirmation modal)."""
    success, message = db.delete_attendance(pk)
    flash(message, "success" if success else "danger")
    return redirect(url_for("attendance"))


# ---------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------

if __name__ == "__main__":
    # Automatically create the database/tables on first launch.
    db.init_db()
    debug_mode = os.environ.get("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug_mode)
