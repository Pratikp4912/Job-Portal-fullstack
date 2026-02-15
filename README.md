# 🚀 Flask Job Portal System

A full-stack Job Portal Web Application built using Flask that allows employers to post job listings, job seekers to browse and apply for jobs, and admins to manage users and job postings.

---

## 📌 Project Overview

This application simulates a real-world job portal system. It includes user authentication, role-based access control, job management, and application tracking features.

The system has three main roles:

- 👤 Job Seeker
- 🏢 Employer
- 🛠 Admin

---

## ✨ Features

### 🔐 Authentication
- User Registration
- Login & Logout
- Secure Password Hashing
- Role-based Access Control

### 🏢 Employer Features
- Post Job Listings
- View Posted Jobs
- Manage Job Listings

### 👤 Job Seeker Features
- Browse Jobs
- View Job Details
- Apply for Jobs
- Prevent Duplicate Applications
- View Applied Jobs

### 🛠 Admin Features
- View All Users
- View All Jobs
- Delete Job Listings

---

## 🛠 Tech Stack

| Technology | Description |
|------------|------------|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| SQLAlchemy | ORM |
| Flask-Login | Authentication |
| HTML | Structure |
| CSS | Styling |
| Bootstrap | Responsive UI |

---
## 📂 Project Structure

job_portal_flask/
│
├── app.py
├── models.py
├── forms.py
├── config.py
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── jobs.html
│ ├── job_detail.html
│ ├── post_job.html
│ ├── my_jobs.html
│ ├── my_applications.html
│ └── admin_dashboard.html
│
├── static/
│ └── css/style.css
│
├── instance/
│ └── jobportal.db
│
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/flask-job-portal-system.git
cd flask-job-portal-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000


