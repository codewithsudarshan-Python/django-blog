# 📝 My Django Blog

A full-featured blog platform built with Django — supporting video and photo posts, category filtering, live search, comments, user authentication, and a detailed analytics dashboard with interactive charts.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

This project is a full-stack blog application built to practice and demonstrate real-world Django development — from authentication and CRUD operations to custom analytics tracking and interactive dashboards.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Signup, login, logout with extended user profiles |
| ✍️ **Post Management** | Create, edit, and delete posts with video or image uploads |
| 🏷️ **Categories** | Filter posts by Travel, Tech, Personal, Food, Lifestyle, Other |
| 🔎 **Live Search** | Instant client-side search by title or category |
| 💬 **Comments** | Authenticated users can comment on any post |
| 📸 **Photo Gallery** | Dedicated gallery view for image posts |
| 👤 **User Profile** | View account details and comment history |
| 📩 **Newsletter** | Email subscription capture |
| 📊 **Analytics Dashboard** | Total visits, unique visitors, new vs. returning, device breakdown, top referrers, most visited pages, post view counts — all with interactive charts |
| 🌗 **Theme Toggle** | Dark/Light mode, persisted per-browser |
| 📱 **Responsive Design** | Fully responsive with Bootstrap 5 |
| 🔧 **Admin Panel** | Full Django admin support |

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript, Chart.js
- **Tools:** Django ORM, Django Auth, Django Admin, Git

---

## 📂 Project Structure

```
myproject/
├── blog/
│   ├── models.py          # Post, UserProfile, Comment, PageVisit, Newsletter
│   ├── views.py            # View logic including analytics
│   ├── urls.py
│   ├── templates/blog/     # All HTML templates
│   └── migrations/
├── media/                  # Uploaded images and videos
├── myproject/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/codewithsudarshan-Python/django-blog.git
   cd django-blog
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django django-bootstrap5
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. Visit **http://127.0.0.1:8000** in your browser 🎉

---

## 📈 Analytics Dashboard

The built-in analytics dashboard tracks:
- Total visits & unique visitors
- New vs. returning visitor breakdown
- Device type (Desktop / Mobile / Tablet)
- Top referrer sources
- Most visited pages
- Post-level view counts

---

## 👤 Author

**Sudarshan**
BBACA Graduate · Aspiring Python/Django Developer
📫 [GitHub](https://github.com/codewithsudarshan-Python)

---

## 📄 License

This project is open source and available for learning purposes under the MIT License.