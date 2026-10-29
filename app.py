
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create the table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Home page: display students and add students
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        course = request.form["course"].strip()
        age = request.form["age"]

        if not name or not email or not course:
            conn.close()
            return "All fields are required.", 400

        try:
            age = int(age)
            if age < 1 or age > 120:
                raise ValueError

            conn.execute(
                "INSERT INTO students (name, email, course, age) "
                "VALUES (?, ?, ?, ?)",
                (name, email, course, age)
            )
            conn.commit()
        except ValueError:
            conn.close()
            return "Enter a valid age between 1 and 120.", 400

        conn.close()
        return redirect(url_for("index"))

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", students=students)

# Update a student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    if student is None:
        conn.close()
        return "Student not found.", 404

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        course = request.form["course"].strip()

        try:
            age = int(request.form["age"])
            if not name or not email or not course:
                raise ValueError
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            conn.close()
            return "Enter valid student details.", 400

        conn.execute("""
            UPDATE students
            SET name = ?, email = ?, course = ?, age = ?
            WHERE id = ?
        """, (name, email, course, age, id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", student=student)

# Delete a student
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
