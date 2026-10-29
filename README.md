Student Management System 🎓

A simple web-based Student Management System built using Python, Flask, SQLite, HTML, and CSS. This project helps manage student records digitally with features to add, view, search, update, and delete student information.

📌 Project Overview

The Student Management System is designed to simplify student record management. It provides a user-friendly web interface to store and manage student information in an SQLite database.

This project is suitable for Python beginners, college mini-projects, and web development practice.

✨ Features
Dashboard: View the total number of registered students.
Add Student: Register students with name, email, age, and course.
View Students: Display all registered student records.
Search Students: Search by name, email, or course.
Update Student: Edit existing student information.
Delete Student: Remove student records with confirmation.
SQL Database: Store records persistently using SQLite.
Input Validation: Validate required fields, age, and email format.
Duplicate Email Prevention: Prevent registration with an existing email address.
Responsive Design: Simple interface for desktop and mobile screens.
🛠️ Technologies Used
Technology	Purpose
Python	Backend programming
Flask	Web framework
SQLite	Database
SQL	Database operations
HTML5	Page structure
CSS3	Styling
Jinja2	Dynamic HTML templates
Git and GitHub	Version control and project hosting
📂 Project Structure
text
Student Management System/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── student_form.html
│
├── static/
│   └── style.css
│
└── students.db


Note: students.db is generated automatically when the application initializes. It is recommended to exclude the database file from Git if it contains personal or sensitive student information.

⚙️ Requirements
Python 3.10 or later
Flask
A web browser
Visual Studio Code 
🚀 Installation and Setup
1. Clone the repository
bash
git clone https://github.com/narendra9346/Student-Management-System


Replace the URL with your actual GitHub repository URL.

2. Navigate to the project directory
bash
cd "Student Management System"

3. Create a virtual environment

On Windows:

powershell
py -m venv .venv

4. Activate the virtual environment

On Windows PowerShell:

powershell
.venv\Scripts\Activate.ps1


If activation is blocked by your system's execution policy, you can use Command Prompt instead:

cmd
.venv\Scripts\activate.bat

5. Install dependencies
powershell
py -m pip install -r requirements.txt


If requirements.txt does not exist, create it and add:

text
Flask>=3.1,<4.0


Then run the installation command again.

6. Run the application
powershell
py app.py

7. Open the application

Open your browser and visit:

http://127.0.0.1:5000

The application should now be running locally.

🗄️ Database Details

The application uses SQLite to store student records.

Students Table
Column	Description
id	Unique student ID
name	Student's full name
email	Unique email address
age	Student's age
course	Student's course
created_at	Record creation timestamp

The database and table are created automatically by the Python application.

🔄 CRUD Operations

The project implements the four basic database operations:

Create: Add a new student.
Read: Display and search student records.
Update: Edit student details.
Delete: Remove a student record.
🔐 Security Notes
SQL queries use parameterized statements to reduce SQL injection risks.
Form inputs are validated before being stored.
Duplicate email addresses are rejected.
This beginner version does not include administrator authentication or CSRF protection.
Before production deployment, add authentication, authorization, CSRF protection, secure secret-key configuration, and appropriate database backups.
Do not commit real student records, passwords, or secret keys to GitHub.
🔮 Future Enhancements
Administrator login and authentication.
Student attendance management.
Examination marks and grade management.
Fee management.
Department and faculty management.
Export records to CSV or Excel.
Student profile photographs.
MySQL database integration.
Reports and analytics.
🎯 Learning Outcomes

By completing this project, you can learn:

Python functions and exception handling.
Flask routes and HTTP methods.
HTML forms and CSS styling.
SQL queries and database integration.
CRUD application development.
Form validation and error handling.
Git and GitHub version control.
👨‍💻 Author

Your Name

GitHub: https://github.com/narendra9346

📄 License

This project is available for educational and learning purposes. Add an appropriate open-source license, such as the MIT License, if you intend to permit others to reuse and distribute your code.

⭐ If you find this project useful, consider giving the repository a star on GitHub!
