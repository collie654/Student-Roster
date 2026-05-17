# Student Roster

A full-stack web application for managing student roster data across school districts.

## Live Demo

- **Frontend:** https://student-roster-production.up.railway.app
- **API Docs:** https://friendly-youthfulness-production.up.railway.app/docs

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + TypeScript (Vite) |
| Backend | Python 3.12 + FastAPI |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 + Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Local Dev | Docker + Docker Compose |
| Production | Railway |
| CI | GitHub Actions |

## Features

- **JWT authentication** — stateless token-based auth with bcrypt password hashing
- **Role-based access control** — read access for all authenticated users; create, update, and delete restricted to admins
- **FERPA-conscious design** — sensitive fields (date of birth) excluded from API responses; access minimized to what clients actually need
- **Full CRUD API** — student and district management with filtering and pagination
- **Auto-generated API docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- **Database migrations** — versioned, reversible schema changes via Alembic
- **CI pipeline** — automated backend tests and TypeScript type checking on every push

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

Docker handles Python, Node, and PostgreSQL — no local installs needed.

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/student-roster.git
cd student-roster
```

### 2. Configure environment

```bash
cp .env.example .env
```

Generate a secret key and paste it into `.env`:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the stack

```bash
docker compose up --build
```

All three services start automatically. The backend runs Alembic migrations on startup.

### 4. Seed the database

In a new terminal:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python seed.py
```

### 5. Open the app

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

**Default credentials:** `admin@roster.dev` / `admin1234`

## Project Structure

```
student-roster/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app + CORS + router includes
│   │   ├── database.py       # SQLAlchemy engine + session factory
│   │   ├── models.py         # ORM models: User, District, Student
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   ├── auth.py           # JWT creation/verification + bcrypt
│   │   ├── dependencies.py   # get_db(), get_current_user(), require_admin()
│   │   └── routers/
│   │       ├── auth.py       # POST /auth/login
│   │       └── students.py   # GET/POST/PATCH/DELETE /students
│   ├── alembic/              # Migration scripts
│   ├── tests/                # pytest integration tests
│   ├── seed.py               # Test data seeder
│   ├── Dockerfile            # Production image (used by Railway)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Root component + auth state
│   │   ├── api.ts            # Centralized API client
│   │   └── pages/
│   │       ├── LoginPage.tsx
│   │       └── StudentsPage.tsx
│   ├── Dockerfile            # Production image (used by Railway)
│   ├── Dockerfile.dev        # Dev server image (used by Docker Compose)
│   └── vite.config.ts
├── .github/
│   └── workflows/
│       └── ci.yml            # Backend tests + frontend type check
├── docker-compose.yml        # Local development stack
├── .env.example
└── README.md
```

## API Reference

### Authentication

```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@roster.dev&password=admin1234
```

Returns an `access_token`. Include it in subsequent requests:

```
Authorization: Bearer <token>
```

### Students

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/students/` | Any user | List students (filterable) |
| GET | `/students/{id}` | Any user | Get a single student |
| POST | `/students/` | Admin only | Create a student |
| PATCH | `/students/{id}` | Admin only | Partially update a student |
| DELETE | `/students/{id}` | Admin only | Delete a student |

### Query Parameters — GET /students/

| Parameter | Type | Description |
|-----------|------|-------------|
| `district_id` | int | Filter by district |
| `grade_level` | int | Filter by grade level |
| `skip` | int | Pagination offset (default: 0) |
| `limit` | int | Max results, up to 200 (default: 50) |

Full interactive documentation at **http://localhost:8000/docs**.

## Development

### Useful commands

```bash
# View logs for a specific service
docker compose logs -f backend

# Run database migrations
docker compose exec backend alembic upgrade head

# Generate a new migration after model changes
docker compose exec backend alembic revision --autogenerate -m "describe the change"

# Open a PostgreSQL shell
docker compose exec db psql -U roster -d roster_db

# Run backend tests
docker compose exec backend pytest tests/ -v

# Wipe the database and start fresh
docker compose down -v && docker compose up --build
```

## Deployment

This project is deployed on [Railway](https://railway.app). Each push to `main` triggers an automatic redeploy.

The project uses two separate Dockerfiles for the frontend:

- `frontend/Dockerfile` — production build using `vite preview`, used by Railway
- `frontend/Dockerfile.dev` — Vite dev server, used by Docker Compose locally

The backend uses a single `Dockerfile` with a dynamic `$PORT` variable that works in both environments.

### Environment variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (default: 30) |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins |
| `ENVIRONMENT` | `development` or `production` |
| `VITE_API_URL` | Backend URL (frontend only) |

## Design Decisions

**Why JWT over server sessions?**
Stateless tokens work without shared session storage, making horizontal scaling straightforward. Short expiry limits the window of risk if a token is compromised.

**Why the same error for wrong email vs wrong password?**
Different errors would allow attackers to enumerate valid email addresses. A single generic 401 response prevents this.

**Why is `date_of_birth` excluded from `StudentResponse`?**
FERPA requires minimizing exposure of student PII. The field is stored for record-keeping but excluded from API responses where it is not needed — data minimization at the schema level.

**Why `condition: service_healthy` instead of `depends_on` alone?**
`depends_on` waits for the container to start, not for PostgreSQL to be ready to accept connections. The healthcheck polls `pg_isready` until the database is actually available, preventing connection errors on startup.

**Why PATCH instead of PUT for updates?**
PATCH applies partial updates — only fields the client sends are changed. `model_dump(exclude_unset=True)` ensures unset fields are not overwritten with `None`.

**Why two frontend Dockerfiles?**
The dev server reads environment variables at runtime, making local development straightforward. The production build bakes variables in at build time. Separating them keeps both environments working correctly without runtime injection hacks.

## What I'd Add Next

- [ ] Refresh token endpoint with httpOnly cookie storage
- [ ] Request-level audit logging middleware (FERPA access logging)
- [ ] District management endpoints and dropdown in the create form
- [ ] Full-text search on student names
- [ ] Rate limiting on the login endpoint
- [ ] Pagination controls in the frontend

## License

MIT