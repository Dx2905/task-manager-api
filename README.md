
# 🗂️ Task Manager API Platform

A Trello-style Task Manager backend built with **FastAPI**, **PostgreSQL**, and **Docker**. It supports **user authentication**, **JWT-based security**, **role-based access (admin/member)**, and full **task CRUD operations**. Designed with scalability and production-readiness in mind.

---

## 🚀 Features

### ✅ Core Functionality
- **User Signup/Login** (`/auth/signup`, `/auth/login`)
- **JWT Auth** with `OAuth2PasswordBearer`
- **Task CRUD** operations (`/tasks/`) with search, pagination, filtering
- **User management** routes (get/update/delete)
- **Admin-only user deletion**
- **Role-based access control (RBAC)** via dependency logic
- **Modular FastAPI structure** (routes, models, schemas, services)

### 🧪 Test Coverage
- Isolated **test database** (`test.db`)
- Fully covered `pytest` suite for:
  - Auth
  - Task CRUD
  - User management
- **No Docker dependency** during test runs
- **CI pipeline** via GitHub Actions

### 📊 Monitoring & Observability
- `/metrics` endpoint with **Prometheus** instrumentation
- Preconfigured **Prometheus dashboard** via Docker
- Logging support (can be extended to file/rotation)

### 🐳 DevOps Ready
- `Dockerfile` for FastAPI app
- `docker-compose.yml` with:
  - PostgreSQL DB
  - Prometheus
- Built-in `.env` support for config
- Production-ready with `uvicorn`, `gunicorn`, or CI pipelines

---

## 🧭 API Endpoints Overview

| Endpoint               | Method | Auth Required | Role    | Description                    |
|------------------------|--------|---------------|---------|--------------------------------|
| `/auth/signup`         | POST   | ❌            | N/A     | Register a new user            |
| `/auth/login`          | POST   | ❌            | N/A     | Login to get JWT token         |
| `/auth/me`             | GET    | ✅            | member  | View current user profile      |
| `/users/{id}`          | GET    | ✅            | self/admin | Get user info             |
| `/users/{id}`          | PUT    | ✅            | self    | Update your profile            |
| `/users/{id}`          | DELETE | ✅            | admin   | Admin deletes a user           |
| `/tasks/`              | POST   | ✅            | member  | Create a task                  |
| `/tasks/`              | GET    | ✅            | member  | List user tasks (search, filter)|
| `/tasks/{id}`          | GET    | ✅            | member  | View a task by ID              |
| `/tasks/{id}`          | PUT    | ✅            | member  | Update a task                  |
| `/tasks/{id}`          | DELETE | ✅            | member  | Delete a task                  |

---

## 🏗️ Project Structure

```bash
task-manager-api/
├── app/
│   ├── api/                # FastAPI routes
│   ├── core/               # App configuration & JWT
│   ├── db/                 # DB session and init
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic (auth, tasks)
│   ├── utils/              # Helper functions (authz, hashing)
│   └── main.py             # Entry point
├── tests/                  # pytest test suite
├── .github/workflows/      # GitHub Actions CI pipeline
├── prometheus.yml          # Prometheus configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md               # You are here
```

---

## 🧪 Running Tests

```bash
# Activate virtualenv first
source venv/bin/activate

# Run all tests
PYTHONPATH=./ pytest -v

# Or run specific test file
PYTHONPATH=./ pytest -v tests/test_users.py
```

Test DB is isolated via SQLite (`test.db`) to allow fast local testing **without Docker**.

---

## 🐳 Run with Docker

```bash
# Build and start
docker-compose up --build

# Access the API
http://localhost:8000/docs

# Prometheus Monitoring
http://localhost:9090

# Metrics Endpoint
http://localhost:8000/metrics
```

Make sure your `.env` contains:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskmanager
SECRET_KEY=your_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🔐 Roles & Permissions

| Role    | Permissions                                    |
|---------|------------------------------------------------|
| member  | Can manage own tasks and update own profile    |
| admin   | Can delete any user, view any user             |

RBAC is enforced using dependency-based authorization (`authz.is_admin_or_self()`).

---

## 📈 Observability & Monitoring

- ✅ `/metrics` endpoint for FastAPI performance
- ✅ Prometheus dashboard at `localhost:9090`
- ⚙️ Logging enabled (can be extended with file/rotation)

---

## 🛠️ GitHub Actions (CI)

- ✅ Automated test pipeline on `push` and `pull_request` to `main`
- Uses Python 3.12 and installs dependencies from `requirements.txt`
- Runs all `pytest` tests with `PYTHONPATH=./` setup

---

## 📘 Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Auth uses JWT via `Bearer` token in Authorization header.

---

## 🤝 Contributing

PRs are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License.

---

## 👨‍💻 Author

**Fnu Gaurav**  
[LinkedIn](https://www.linkedin.com/in/fnu-gaurav-653355252/) • gaurav.yadav2905@gmail.com

---
```

---

