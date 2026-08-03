"""
database.py
-----------
All database-related code lives here: connecting to SQLite, creating
tables, and every CRUD (Create / Read / Update / Delete) helper used
by app.py.

Keeping the database logic separate from the Flask routes (app.py)
makes the project easier to read, test, and maintain - a good habit
for beginners to pick up early.
"""

import sqlite3
from datetime import date

DATABASE_NAME = "attendance.db"


def get_db_connection():
    """
    Open a new connection to the SQLite database.

    `row_factory = sqlite3.Row` lets us access columns by name
    (e.g. row["name"]) instead of by numeric index, which makes the
    code in app.py and the templates much easier to read.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints (off by default in SQLite)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Create the `students` and `attendance` tables if they do not
    already exist. This function is called once when the Flask app
    starts, so the database is set up automatically on first launch.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Attendance table
    # student_id here is a FOREIGN KEY pointing to students.id (the
    # internal primary key, not the human-readable student_id text field)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------
# STUDENT CRUD HELPERS
# ---------------------------------------------------------------------

def get_all_students(search_query=None, class_filter=None):
    """
    Return every student, optionally filtered by a search term
    (matches name or student_id) and/or a class name.
    Uses parameterized queries throughout to prevent SQL injection.
    """
    conn = get_db_connection()
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE ? OR student_id LIKE ?)"
        like_term = f"%{search_query}%"
        params.extend([like_term, like_term])

    if class_filter:
        query += " AND class = ?"
        params.append(class_filter)

    query += " ORDER BY name ASC"

    students = conn.execute(query, params).fetchall()
    conn.close()
    return students


def get_student_by_id(student_pk):
    """Fetch a single student by their internal primary key (id)."""
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_pk,)
    ).fetchone()
    conn.close()
    return student


def get_distinct_classes():
    """Return a sorted list of every unique class name (for filter dropdowns)."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT DISTINCT class FROM students ORDER BY class ASC"
    ).fetchall()
    conn.close()
    return [row["class"] for row in rows]


def add_student(student_id, name, student_class, email, phone):
    """
    Insert a new student record.
    Returns (success: bool, message: str) so app.py can flash the result.
    """
    conn = get_db_connection()
    try:
        conn.execute(
            """INSERT INTO students (student_id, name, class, email, phone)
               VALUES (?, ?, ?, ?, ?)""",
            (student_id, name, student_class, email, phone),
        )
        conn.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        # Happens when student_id already exists (UNIQUE constraint)
        return False, f"Student ID '{student_id}' already exists."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def update_student(pk, student_id, name, student_class, email, phone):
    """Update an existing student's details."""
    conn = get_db_connection()
    try:
        conn.execute(
            """UPDATE students
               SET student_id = ?, name = ?, class = ?, email = ?, phone = ?
               WHERE id = ?""",
            (student_id, name, student_class, email, phone, pk),
        )
        conn.commit()
        return True, "Student updated successfully."
    except sqlite3.IntegrityError:
        return False, f"Student ID '{student_id}' already exists."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def delete_student(pk):
    """Delete a student and (via ON DELETE CASCADE) their attendance records."""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM students WHERE id = ?", (pk,))
        conn.commit()
        return True, "Student deleted successfully."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


# ---------------------------------------------------------------------
# ATTENDANCE CRUD HELPERS
# ---------------------------------------------------------------------

def mark_attendance(student_pk, attendance_date, status, remarks):
    """
    Record attendance for a student on a given date.
    If a record for that student + date already exists, update it
    instead of creating a duplicate (keeps one record per student/day).
    """
    conn = get_db_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM attendance WHERE student_id = ? AND attendance_date = ?",
            (student_pk, attendance_date),
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE attendance SET status = ?, remarks = ? WHERE id = ?",
                (status, remarks, existing["id"]),
            )
            message = "Attendance updated for this date."
        else:
            conn.execute(
                """INSERT INTO attendance (student_id, attendance_date, status, remarks)
                   VALUES (?, ?, ?, ?)""",
                (student_pk, attendance_date, status, remarks),
            )
            message = "Attendance recorded successfully."

        conn.commit()
        return True, message
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def get_attendance_records(date_filter=None, class_filter=None, status_filter=None):
    """
    Return attendance records joined with student info, optionally
    filtered by date, class, and/or status.
    """
    conn = get_db_connection()
    query = """
        SELECT attendance.id, attendance.attendance_date, attendance.status,
               attendance.remarks, students.id AS student_pk,
               students.student_id, students.name, students.class
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE 1=1
    """
    params = []

    if date_filter:
        query += " AND attendance.attendance_date = ?"
        params.append(date_filter)

    if class_filter:
        query += " AND students.class = ?"
        params.append(class_filter)

    if status_filter:
        query += " AND attendance.status = ?"
        params.append(status_filter)

    query += " ORDER BY attendance.attendance_date DESC, students.name ASC"

    records = conn.execute(query, params).fetchall()
    conn.close()
    return records


def get_attendance_by_id(attendance_pk):
    """Fetch a single attendance record by its id."""
    conn = get_db_connection()
    record = conn.execute(
        "SELECT * FROM attendance WHERE id = ?", (attendance_pk,)
    ).fetchone()
    conn.close()
    return record


def update_attendance(attendance_pk, status, remarks):
    """Update the status/remarks of an existing attendance record."""
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE attendance SET status = ?, remarks = ? WHERE id = ?",
            (status, remarks, attendance_pk),
        )
        conn.commit()
        return True, "Attendance record updated successfully."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def delete_attendance(attendance_pk):
    """Delete a single attendance record."""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM attendance WHERE id = ?", (attendance_pk,))
        conn.commit()
        return True, "Attendance record deleted successfully."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def get_todays_attendance_for_students():
    """
    Return a dict mapping student.id -> today's attendance status.
    Used on the 'Mark Attendance' page so we can show each student's
    current status for today.
    """
    conn = get_db_connection()
    today = date.today().isoformat()
    rows = conn.execute(
        "SELECT student_id, status FROM attendance WHERE attendance_date = ?",
        (today,),
    ).fetchall()
    conn.close()
    return {row["student_id"]: row["status"] for row in rows}


# ---------------------------------------------------------------------
# DASHBOARD STATISTICS
# ---------------------------------------------------------------------

def get_dashboard_stats():
    """
    Calculate the statistics shown on the dashboard:
    total students, present today, absent today, attendance percentage.
    """
    conn = get_db_connection()
    today = date.today().isoformat()

    total_students = conn.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    present_today = conn.execute(
        "SELECT COUNT(*) AS count FROM attendance WHERE attendance_date = ? AND status = 'Present'",
        (today,),
    ).fetchone()["count"]

    absent_today = conn.execute(
        "SELECT COUNT(*) AS count FROM attendance WHERE attendance_date = ? AND status = 'Absent'",
        (today,),
    ).fetchone()["count"]

    conn.close()

    marked_today = present_today + absent_today
    attendance_percentage = (
        round((present_today / marked_today) * 100, 1) if marked_today > 0 else 0
    )

    return {
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
        "attendance_percentage": attendance_percentage,
    }
