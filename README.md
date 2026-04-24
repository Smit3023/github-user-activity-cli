# 🐙 GitHub Activity Viewer

> A **Django web application** that fetches and displays any GitHub user's recent activity — commits, pull requests, issues, stars, forks, and more — in a clean, card-based UI using the **GitHub REST API**.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Application Flow](#-application-flow)
- [Supported Event Types](#-supported-event-types)
- [Getting Started](#-getting-started)
- [URL Routes](#-url-routes)

---

## 📖 About the Project

GitHub Activity Viewer is a **web-based tool** that lets anyone look up a GitHub username and instantly see their recent public activity — no login or API token required for basic usage.

It calls the **GitHub Events API** (`/users/{username}/events`) and the **GitHub Users API** (`/users/{username}`) to fetch and display a profile card alongside the last 10 activity events, formatted with icons and human-readable descriptions.

This project demonstrates skills in **external API integration, HTTP request handling without third-party libraries, Django views, template rendering, and Bootstrap UI design**.

---

## 🧰 Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Backend     | Python 3.10+, Django 6.0                |
| API         | GitHub REST API (no auth token needed)  |
| HTTP Client | Python built-in `urllib` (no requests library) |
| Frontend    | Django Templates, Bootstrap 5.3         |
| Database    | SQLite (Django default — not actively used) |

---

## ✅ Features

- 🔍 **Search any GitHub username** via a simple form
- 👤 **User profile card** — avatar, name, followers, following, public repos count
- 📋 **Last 10 activity events** displayed as styled cards
- 🎯 **Human-readable event descriptions** with emoji icons per event type
- ❌ **Error handling** — shows a clear message if a username doesn't exist
- ⚡ **Loading feedback** — Search button text changes to "Loading..." on click
- 📱 **Responsive UI** built with Bootstrap 5

---

## 📁 Project Structure

```
github-user-activity-cli-main/
│
└── github_web/                        # Django root
    │
    ├── activity/                      # Main Django app
    │   ├── views.py                   # API calls + event formatting logic
    │   ├── urls.py                    # App-level URL routing
    │   ├── models.py                  # Empty (no DB models needed)
    │   ├── apps.py
    │   └── templates/
    │       └── activity/
    │           └── index.html         # Single-page UI (search + results)
    │
    ├── github_web/                    # Django project config
    │   ├── settings.py
    │   ├── urls.py                    # Root URL routing
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── manage.py
    └── db.sqlite3
```

---

## 🔄 Application Flow

```
User visits  http://127.0.0.1:8000/
        │
        ▼
   index.html renders (blank search form)
        │
        │  User types a GitHub username & clicks Search
        │
        ▼
   POST /  ──▶  home() view
        │
        ├──▶  fetch_profile(username)
        │         └──▶  GET https://api.github.com/users/{username}
        │                    └── Returns: avatar, name, followers, repos count
        │
        └──▶  fetch_activity(username)
                  └──▶  GET https://api.github.com/users/{username}/events
                             └── Returns: last 30 public events
                                    │
                                    ▼
                             Takes first 10 events
                             Maps each to icon + human-readable text
                                    │
                                    ▼
                        ┌──────────┴──────────┐
                        │  User found?         │
                       Yes                    No
                        │                     │
                  Renders profile        Shows error:
                  card + event cards     "❌ User not found"
```

---

## 🎯 Supported Event Types

The app recognises and formats the following GitHub event types:

| Event Type           | Icon | Description Shown                        |
|----------------------|------|-------------------------------------------|
| `PushEvent`          | 📌   | Pushed commits to `{repo}`               |
| `PullRequestEvent`   | 🔀   | Opened a pull request in `{repo}`        |
| `IssuesEvent`        | 🐛   | Worked on issues in `{repo}`             |
| `IssueCommentEvent`  | 💬   | Commented on an issue in `{repo}`        |
| `CreateEvent`        | 🆕   | Created something in `{repo}`            |
| `DeleteEvent`        | 🗑️   | Deleted something in `{repo}`            |
| `WatchEvent`         | ⭐   | Starred `{repo}`                         |
| `ForkEvent`          | 🍴   | Forked `{repo}`                          |
| Any other event      | 🔹   | `{EventType}` in `{repo}`               |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/github-user-activity-cli.git
cd github-user-activity-cli/github_web

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install Django
pip install django

# 4. Apply migrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — type any GitHub username and hit Search.

> **Note:** No API token is required. The GitHub public API allows unauthenticated requests up to **60 requests/hour** per IP. For higher limits, you can add a GitHub personal access token as an `Authorization` header in `views.py`.

---

## 🌐 URL Routes

| URL       | View   | Description                        |
|-----------|--------|------------------------------------|
| `/`       | `home` | Search form + activity results     |
| `/admin/` | Django Admin | Default Django admin panel  |

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

