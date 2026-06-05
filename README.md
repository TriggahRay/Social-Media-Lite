<div align="center">

# ⚡ Thee Social

### A Full-Stack Social Media Web Application

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pytest](https://img.shields.io/badge/Pytest-34%20Tests-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

**Thee Social** is a feature-complete social media platform built with Django, demonstrating the practical integration of client-side and server-side scripting, secure session management, AJAX-driven interactions, and real-time notifications.

[Live Demo](#) · [Report Bug](../../issues) · [Request Feature](../../issues)

---

![Thee Social Preview](docs/preview.png)

</div>

---

## 📋 Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Security](#security)
- [Testing](#testing)
- [Team](#team)
- [Acknowledgements](#acknowledgements)

---

## 🌐 About The Project

Thee Social is a full-stack social media web application developed as a capstone project for the **Advanced Software Development V (SOD517C)** module at the **Central University of Technology, Free State**. The project was built to demonstrate mastery of full-stack web development concepts including the **Model-View-Template (MVT)** architectural pattern, AJAX-driven dynamic content, dual-layer data validation, session management, and database query optimisation.

---

## ✨ Features

### 👤 Authentication & Profiles
- User registration with dual-layer validation (client-side regex + server-side Django forms)
- Secure login and logout with session management (30-minute inactivity timeout)
- Profile pages with bio, avatar upload, follower/following counts, and post grid
- Role-based access control (User / Admin)

### 📝 Posts
- Create text posts and image posts with visibility control (Public / Followers / Private)
- Hashtag tagging with clickable tags
- Edit and delete own posts
- Paginated news feed showing posts from followed users

### ❤️ Social Interactions (All AJAX -no page reloads)
- Like and unlike posts with instant count update
- Comment on posts with real-time rendering
- Follow and unfollow users with instant button toggle
- Suggested users sidebar on the news feed

### 🔔 Notifications
- Auto-created notifications for likes, comments, and follows via Django Signals
- Unread badge count polled every 30 seconds via AJAX
- Notifications marked as read on visit

### 💬 Direct Messaging
- Full inbox with conversation list and latest message preview
- Real-time chat interface with AJAX message sending
- Messages marked as read when conversation is opened

### 🔍 Live Search
- AJAX-powered live search dropdown in the navbar
- Searches users by username and bio, posts by content and hashtags
- Results appear after 2 characters — no page reload

### 🛡️ Admin Panel
- Full Django admin panel at `/admin/`
- Manage users, moderate posts, view activity logs, manage tags

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML5, CSS3, JavaScript (ES6+) | Structure, styling, interactivity |
| UI Framework | Bootstrap 5 | Responsive dark-themed design |
| Dynamic Content | AJAX Fetch API | Likes, comments, follows, search |
| Backend | Python 3.11 + Django 4.2 | MVT architecture, routing, business logic |
| Database | SQLite | Persistent relational data storage |
| ORM | Django ORM | Parameterised query generation |
| Authentication | Django Auth + PBKDF2-SHA256 | Sessions, password hashing |
| Validation | Django Forms + Regex | CSRF protection, input sanitisation |
| Image Handling | Pillow | Profile pictures, post image processing |
| Notifications | Django Signals | Auto-trigger on social events |
| Testing | Pytest-Django | 34 automated tests |
| Version Control | Git + GitHub | Source control, collaboration |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.11+](https://python.org/downloads/)
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/) (recommended)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/thee-social.git
cd thee-social
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Apply database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a superuser (for the admin panel)**
```bash
python manage.py createsuperuser
```

**6. Create the media folder**
```bash
mkdir media
mkdir media/profile_pics
```

### Running the App

```bash
python manage.py runserver
```

Then open your browser and visit:

| URL | Page |
|---|---|
| `http://127.0.0.1:8000/register/` | Register a new account |
| `http://127.0.0.1:8000/login/` | Login |
| `http://127.0.0.1:8000/` | News feed |
| `http://127.0.0.1:8000/admin/` | Admin panel |

---

## 📁 Project Structure

```
thee-social/
│
├── socialmedia/              # Project settings and root URL config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                 # User auth, profiles, registration
│   ├── models.py             # Custom User model
│   ├── views.py              # Register, login, logout, profile
│   ├── forms.py              # RegisterForm, LoginForm, ProfileEditForm
│   ├── urls.py
│   └── tests.py              # 8 unit tests
│
├── posts/                    # Post creation, feed, detail
│   ├── models.py             # Post, Tag, PostTag
│   ├── views.py              # Feed, create, edit, delete
│   ├── forms.py              # PostForm
│   ├── urls.py
│   └── tests.py              # 8 unit tests
│
├── social/                   # Likes, comments, follows, notifications
│   ├── models.py             # Like, Comment, Follow, Notification
│   ├── views.py              # AJAX like, comment, follow, notifications
│   ├── signals.py            # Auto-create notifications on social events
│   ├── urls.py
│   └── tests.py              # 10 unit tests
│
├── messaging/                # Direct messages, inbox, search
│   ├── models.py             # Message
│   ├── views.py              # Inbox, conversation, send, search
│   ├── urls.py
│   └── tests.py              # 8 unit tests
│
├── templates/                # All HTML templates
│   ├── base.html             # Base layout with navbar
│   ├── accounts/
│   ├── posts/
│   ├── social/
│   └── messaging/
│
├── static/
│   └── css/
│       └── style.css         # Dark theme stylesheet
│
├── media/                    # User uploaded files (gitignored)
│   └── profile_pics/
│
├── conftest.py               # Pytest fixtures
├── pytest.ini                # Pytest configuration
├── manage.py
└── requirements.txt
```

---

## 🗃️ Database Schema

The application uses **9 tables normalised to Third Normal Form (3NF)**:

```
User ──────┬──── Post ────┬──── Comment
           │              ├──── Like
           │              ├──── PostTag ──── Tag
           │              └──── Notification
           ├──── Follow
           └──── Message
```

| Table | Purpose |
|---|---|
| `User` | Extended AbstractUser with bio, avatar, role |
| `Post` | Text/image posts with visibility settings |
| `Comment` | Post comment threads |
| `Like` | Toggle-based post likes (UNIQUE constraint) |
| `Follow` | Directed follow relationships (UNIQUE constraint) |
| `Notification` | Social event alerts (like, comment, follow, message) |
| `Message` | Direct user-to-user messages |
| `Tag` | Unique hashtag definitions |
| `PostTag` | Many-to-many post–tag junction table |

---

## 🔒 Security

| Threat | Mitigation |
|---|---|
| SQL Injection | Django ORM parameterised queries - no raw SQL |
| Cross-Site Scripting (XSS) | Django auto-escapes all template variables |
| Cross-Site Request Forgery | CSRF middleware - token required on all POST requests |
| Authentication Bypass | `@login_required` on all protected views |
| Weak Passwords | PBKDF2-SHA256 hashing + strength validation |
| Malicious File Uploads | Pillow MIME type validation server-side |
| Session Hijacking | HttpOnly + Secure cookie flags, 30-min timeout |

---

## 🧪 Testing

The project includes a **34-test automated test suite** built with Pytest-Django.

```bash
# Run all tests
py -m pytest -v

# Run tests for a specific app
py -m pytest accounts/tests.py -v
py -m pytest posts/tests.py -v
py -m pytest social/tests.py -v
py -m pytest messaging/tests.py -v

# Run with coverage
pip install pytest-cov
py -m pytest --cov=. --cov-report=term-missing
```

### Test Coverage

| App | Tests | Coverage |
|---|---|---|
| `accounts` | 8 | Registration, login, logout, profile, session |
| `posts` | 8 | Feed, create, detail, edit, delete, ownership |
| `social` | 10 | Likes, comments, follows, notifications, signals |
| `messaging` | 8 | Inbox, conversation, send message, search |
| **Total** | **34** | All core features and security controls |

---

## 👥 Team

This project was built by a group of 4 students as part of SOD517C at CUT Free State.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- Central University of Technology, Free State

---

<div align="center">


</div>
