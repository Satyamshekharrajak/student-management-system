📘 Student Management System

📖 Overview

The Student Management System is a desktop application built with Python Tkinter for the GUI and SQLite as the database.
It provides a simple yet effective way to manage student records: add, update, delete, view, and search students.

The app demonstrates:

Database integration with SQLite (local, serverless DB).

CRUD operations (Create, Read, Update, Delete).

Modern Tkinter-based user interface with Treeview.

Real-world project structure for beginner DevOps / Python projects.

🏗️ Features

Add Student – Register new students with details (name, enrollment, course, etc.).

View Students – Display all students in a scrollable Treeview table.

Update Student – Edit existing student information.

Delete Student – Remove students from the database.

Search Student – Filter records by enrollment, phone, or email.

Reset Form – Clear the input fields.

SQLite Backend – Portable, no server required.

📂 Project Structure

student_management_system/
│
├── student_management_system.db   # SQLite database (auto-created on first run)
├── student_management.py          # Main Python script (GUI + logic)
└── README.md                      # Project documentation (this file)

▶️ Running the Application

python student_management.py

On first run, a SQLite database file student_management_system.db will be created with a student table.

🗄️ Database Schema

The table student contains:

Column	        Type	Description1
Enrollment	    TEXT	Primary Key (Unique ID)
Name	        TEXT	Student’s full name
Course	        TEXT	Course enrolled
Department	    TEXT	Department name
Year	        TEXT	Academic year
Semester	    TEXT	Current semester
Section	        TEXT	Section / branch
Gender	        TEXT	Gender
DOB	            TEXT	Date of birth
Phone	        TEXT	Contact number
Email	        TEXT	Email ID
Address	        TEXT	Address

