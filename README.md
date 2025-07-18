# 🎫 Flask Support Ticket System

A simple and secure support ticketing system built with Flask and SQLite. It allows users to raise issues and track their status, while admins can manage and resolve those tickets via a web interface.

---

## 📸 Screenshots

### 🔐 Login Page
![Login Page](images/login_page.png)

### 🔐 Registration Page
![Registration Page](images/registration_form.png)

### 👤 User Dashboard
![User Dashboard](images/user_dashboard.png)

### 🔐 Admin Dashboard
![Admin Page](images/admin_panel.png)

### 🔐 Ticket Filtering Form
![Ticket Filtering Form](images/ticket_filtering_form.png)

### 🔐 Create Ticket Form
![Create Ticket Form](images/create_ticket_form.png)

---

## 🚀 Features

- 🔐 User registration & secure login (hashed passwords)
- 🎫 Raise, view, and filter tickets by status
- 📊 Admin panel to view, assign, and update tickets
- 🛡️ Role-based access control (`user` and `admin`)
- ✅ Session management for authentication
- 📦 SQLite database integration with SQLAlchemy ORM

---

## 🛠️ Tech Stack

- **Backend:** Flask
- **Database:** SQLite (via SQLAlchemy)
- **Frontend:** HTML, Jinja2 Templates
- **Security:** Werkzeug for password hashing

---

## ⚙️ Getting Started

### 1. Clone the Repository

### Assumption 
#### To create admin userID and Password
```bash
python .\adminUser.py

Then to run the project:

git clone https://github.com/yourusername/flask-ticket-system.git
cd flask-ticket-system

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
python app.py

Visit http://127.0.0.1:5000 in your browser.