# 🚀 Task & Team Management API

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

A high-performance, secure, and production-ready REST API for managing Projects, Teams, and Members. Designed to serve as the backend engine for modern collaborative workspaces.

## ✨ Key Features

- **🔐 Robust Authentication**: Token-based authentication using Django REST Framework.
- **🛡️ Object-Level Security**: Custom permission classes (`IsTeamLeader`, `IsProjectCreator`) ensuring that users can only modify resources they own or control.
- **⚡ Lightning Fast Caching**: Heavily-accessed endpoints (Profiles, Projects, Teams) are cached via **Redis**, with cache bucketing strictly isolated per user token.
- **🚀 Production Ready**: Pre-configured with `gunicorn`, `whitenoise` (for static file serving), and dynamic Postgres database bindings (`dj-database-url`).
- **🌐 Cross-Origin Ready**: Seamless `django-cors-headers` integration for easy connections to React/Vue/Next.js frontends.

---

## 🛠️ Architecture

The backend is split into three highly cohesive Django apps:
1. `register`: Handles User Auth, Token Generation, and User Profiles.
2. `project`: Handles the creation and management of Projects.
3. `teams`: Handles Team creation, role assignments (Leaders vs. Members), and linking Teams to Projects.

---

## 🚀 Quick Start (Local Development)

**1. Clone the repository and navigate to the project directory**

**2. Create a virtual environment & install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Copy the template file to create your own configuration:
```bash
cp .env.example .env
```
*(Optionally, set `REDIS_URL` in `.env` to connect to a local or remote Redis instance. Otherwise, it safely falls back to local memory!)*

**4. Run Migrations & Start Server**
```bash
python manage.py migrate
python manage.py runserver
```

---

## ☁️ Deployment (Render / Heroku)

This API is pre-configured for instant deployment on PaaS providers like Render.

### Render Setup:
1. Connect your GitHub repository to Render as a **Web Service**.
2. **Build Command**: `./build.sh` *(This installs dependencies, collects static files, and runs migrations)*
3. **Start Command**: `daphne task_management.asgi:application --port $PORT --bind 0.0.0.0`
4. Add the following **Environment Variables** in Render's dashboard:
   - `SECRET_KEY` (Generate a random secure string)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*` (or your Render URL)
   - `CORS_ALLOWED_ORIGINS` = `*` (or your frontend URL)
   - `DATABASE_URL` (Connect to your Render PostgreSQL database)
   - `REDIS_URL` (Connect to Upstash or Render Redis)

---

## 📚 API Endpoints

### Auth / Profiles (`/api/auth/`)
- `POST /register/`: Register a new user.
- `POST /login/`: Obtain Auth Token.
- `GET /profile/`: List all profiles *(Cached)*.
- `GET /profile/me/`: Retrieve/Update/Delete your own profile.

### Projects (`/api/projects/`)
- `GET /`: List all public projects *(Cached)*.
- `POST /my-projects/`: Create a new project.
- `PUT /my-projects/{id}/`: Update your own project *(Secured)*.

### Teams (`/api/teams/`)
- `GET /`: List all teams *(Cached)*.
- `POST /`: Create a new team (You become the leader automatically).
- `PUT /delete/{id}/`: Manage the team *(Requires Leader)*.
- `POST /members/add/`: Add a user to a team *(Requires Leader)*.
- `DELETE /members/{id}/`: Remove a user from a team *(Requires Leader)*.
