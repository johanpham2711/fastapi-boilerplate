# <p style="text-align: center">FastAPI Boilerplate</p>

<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; text-align: center;">

  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge" alt="Pydantic" />
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres" />
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white" alt="Swagger" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT" />
  <img src="https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black" alt="Jinja" />
  <img src="https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3" alt="Pytest" />
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres" />

</div>

## Description

[FastAPI Boilerplate](https://github.com/johanpham2711/fastapi-boilerplate) with [FastAPI](https://fastapi.tiangolo.com/#installation), [Postgres](https://www.postgresql.org/),...

by [Johan Pham](https://github.com/johanpham2711)

## Tech Stack

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Database
- **SQLAlchemy 2.0** - Async ORM
- **Redis** - Caching and message broker
- **Arq** - Background jobs
- **JWT** - Authentication
- **Pydantic V2** - Data validation
- **Alembic** - Database migrations
- **aiosmtplib** - Email sending
- **Jinja2** - Email templates
- **pytest** - Testing
- **ruff** - Linting
- **mypy** - Type checking
- **black** - Code formatting
- **uv** - Package management

## Project Structure

```
fastapi-boilerplate/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth/          # Authentication endpoints
│   │       ├── users/         # User management endpoints
│   │       └── templates/    # Template endpoints
│   ├── core/                  # Core configuration
│   │   ├── config.py         # Settings
│   │   ├── database.py       # Database connection
│   │   ├── security.py       # JWT & password hashing
│   │   └── arq_config.py     # Background jobs config
│   ├── models/               # SQLAlchemy models
│   ├── services/             # Business logic
│   │   ├── user_service.py
│   │   ├── template_service.py
│   │   ├── email_service.py
│   │   └── background_tasks.py
│   ├── repositories/         # Data access layer
│   ├── templates/            # Email templates
│   └── main.py              # FastAPI app
├── tests/                    # Test files
├── alembic/                  # Database migrations
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (recommended)
- uv (package manager) - `pip install uv`

### Virtual Environment

It's recommended to use a dedicated virtual environment for this project.

Recommended (uv):

```bash
# Create a virtual environment in .venv
uv venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Alternative (built-in venv):

```bash
# Create a virtual environment in .venv
python -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

To deactivate at any time:

```bash
deactivate
```

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/johanpham2711/fastapi-boilerplate
cd fastapi-boilerplate
```

2. **Install dependencies**:

```bash
uv pip install -e ".[dev]"
```

3. **Copy environment file**:

```bash
cp env.example .env
```

4. **Update `.env` with your configuration**:

```bash
# Edit .env file with your settings
```

5. **Start Docker containers**:

```bash
make docker-up
# or
docker compose up -d
```

6. **Run database migrations**:

```bash
alembic upgrade head
```

7. **Start development server**:

```bash
make dev
# or
uvicorn app.main:app --reload
```

8. **Open your browser**:

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Commands

```bash
# Install dependencies
make install

# Run development server
make dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Lint code
make lint

# Format code
make format

# Start Docker containers
make docker-up

# Stop Docker containers
make docker-down

# View Docker logs
make docker-logs

# Clean build artifacts
make clean
```

## Features

- ✅ JWT Authentication with refresh tokens
- ✅ User management (CRUD)
- ✅ Template management (CRUD)
- ✅ Background jobs with Arq
- ✅ Email service with SMTP
- ✅ Redis caching
- ✅ SQLAlchemy async ORM
- ✅ Database migrations with Alembic
- ✅ API documentation (Swagger/OpenAPI)
- ✅ Comprehensive testing with pytest
- ✅ Docker support
- ✅ Pre-commit hooks for code quality
- ✅ Code quality tools (ruff, mypy, black)

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Users

- `POST /api/users/` - Create user
- `GET /api/users/` - List users
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Templates

- `POST /api/templates/` - Create template
- `GET /api/templates/` - List templates
- `GET /api/templates/{id}` - Get template by ID
- `PUT /api/templates/{id}` - Update template
- `DELETE /api/templates/{id}` - Delete template

## Development

### Setup Pre-commit Hooks

```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration status
alembic current
```

### Background Jobs (Arq)

To run background jobs worker:

```bash
arq app.services.background_tasks.WorkerSettings
```

## Environment Variables

See `env.example` for all available environment variables.

### Key Variables

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port
- `SMTP_HOST` - SMTP server host
- `SMTP_USERNAME` - SMTP username
- `SMTP_PASSWORD` - SMTP password

## Docker

### Development

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Production

Modify `docker-compose.yml` for production settings:

- Use proper secrets management
- Enable SSL/TLS
- Configure production database
- Set up reverse proxy (nginx)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code Quality

This project uses:

- **ruff** - Fast Python linter
- **mypy** - Static type checking
- **black** - Code formatter
- **pre-commit** - Git hooks
- **commitizen** - Commit message convention

## License

MIT

## Author

Johan Pham

## Acknowledgments

- Inspired by [benavlabs/FastAPI-boilerplate](https://github.com/benavlabs/fastapi-boilerplate)
- Built with modern Python async stack
