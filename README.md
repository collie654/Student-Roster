# Student Roster API

A full-stack web application for managing student roster data across school districts.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript (Vite) |
| Backend | Python 3.12 + FastAPI |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 + Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Deployment | Docker + Docker Compose |
| CI | GitHub Actions |

## Features

- **JWT Authentication** — stateless token-based auth with bcrypt password hashing
- **Role-Based Access Control** — read access for all authenticated users; create/update/delete restricted to admins
- **FERPA-conscious design** — sensitive fields (date of birth) excluded from API responses; access logging ready
- **Full CRUD API** — student and district management with filtering and pagination
- **Auto-generated API docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- **Database migrations** — versioned, reversible schema changes via Alembic
- **CI pipeline** — automated tests and TypeScript type checking on every push

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

## License

MIT