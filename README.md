# 🎟️ Ticket Shop

is a Django-based web application that simulates an online ticket booking system for events .

## 📌 Overview

**Ticket Shop** allows users to:
- Browse available tickets
- Add tickets to their cart
- Manage orders via user panel
- Authenticate and manage their profile
- Admins can manage tickets, users, and events

---

## 🚀 Features

- 🔐 User registration and login
- 🛒 Shopping cart system
- 📅 Event and ticket management
- 👤 User dashboard to manage orders
- 🛠 Admin panel
- ⏰ Background tasks using Celery
- 🧱 Modular structure with multiple Django apps

---

## 🛠 Technologies Used

- Python 3
- Django
- SQLite (default database)
- Celery (for async tasks)
- HTML Templates
- Django Admin

---

## 📁 Project Structure
 
 ```
Ticket_Shop/
├── accounts/ # Authentication and user management
├── cart/ # Shopping cart and order handling
├── events/ # Event and ticket models
├── panel/ # User profile/dashboard
├── home/ # Public-facing views and homepage
├── templates/ # HTML templates and statics files
├── Ticket_Shop/ # Project settings and routing
├── manage.py
└── utils.py
```
---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ARASwithH/Ticket_Shop.git
cd Ticket_Shop
```

### 2. Set Up Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

---
## 🔐 Admin Panel
Access the admin interface at /admin/ using your superuser credentials.

From here you can manage:
* Users and profiles
* Orders, Discount codes, Payments and Tickets
* Events and Categories
* Periodic Tasks
