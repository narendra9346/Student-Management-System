
import os
import sqlite3
from pathlib import Path

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, abort
)

app = Flask(__name__)

# Use an environment variable for the secret key in production.
app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-key-change-before-deployment"
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"


# Connect to the SQLite database
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Create the students table automatically
def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                age INTEGER NOT NULL CHECK(age BETWEEN 1 AND 120),
                course TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


# Dashboard and student search
@app.route("/")
def index():
    search = request.args.get("q", "").strip()

    with get_db() as db:
        total = db.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        if search:
            pattern = f"%{search}%"
            students = db.execute("""
                SELECT * FROM students
                WHERE name LIKE ?
                   OR email LIKE ?
                   OR course LIKE ?
                ORDER BY id DESC
            """, (pattern, pattern, pattern)).fetchall()
        else:
            students = db.execute("""
                SELECT * FROM students
                ORDER BY id DESC
            """).fetchall()

    return render_template(
        "index.html",
        students=students,
        total=total,
        search=search
    )


# Validate student form data
def get_student_form():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    age_text = request.form.get("age", "").strip()
    course = request.form.get("course", "").strip()

    if not name or not email or not age_text or not course:
        return None, "All fields are required."

    if len(name) > 100 or len(email) > 254 or len(course) > 100:
        return None, "Please shorten the entered information."

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return None, "Please enter a valid email address."

    try:
        age = int(age_text)
    except ValueError:
        return None, "Age must be a whole number."

    if not 1 <= age <= 120:
        return None, "Age must be between 1 and 120."

    return {
        "name": name,
        "email": email,
        "age": age,
        "course": course
    }, None


# Add a new student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student, error = get_student_form()

        if error:
            flash(error, "error")
            return render_template(
                "student_form.html",
                student=request.form,
                page_title="Add Student"
            )

        try:
            with get_db() as db:
                db.execute("""
                    INSERT INTO students (name, email, age, course)
                    VALUES (?, ?, ?, ?)
                """, (
                    student["name"],
                    student["email"],
                    student["age"],
                    student["course"]
                ))
            flash("Student added successfully!", "success")
            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            flash("This email address is already registered.", "error")

    return render_template(
        "student_form.html",
        student={},
        page_title="Add Student"
    )


# Edit an existing student
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db() as db:
        student = db.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if student is None:
        abort(404)

    if request.method == "POST":
        updated, error = get_student_form()

        if error:
            flash(error, "error")
            return render_template(
                "student_form.html",
                student=request.form,
                page_title="Edit Student"
            )

        try:
            with get_db() as db:
                db.execute("""
                    UPDATE students
                    SET name = ?, email = ?, age = ?, course = ?
                    WHERE id = ?
                """, (
                    updated["name"],
                    updated["email"],
                    updated["age"],
                    updated["course"],
                    student_id
                ))
            flash("Student updated successfully!", "success")
            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            flash("That email address belongs to another student.", "error")
            return render_template(
                "student_form.html",
                student=request.form,
                page_title="Edit Student"
            )

    return render_template(
        "student_form.html",
        student=student,
        page_title="Edit Student"
    )


# Delete a student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            abort(404)

    flash("Student deleted successfully.", "success")
    return redirect(url_for("index"))


# Initialize the database and start the app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
