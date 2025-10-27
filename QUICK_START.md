# 🚀 Quick Start Guide

## ✅ Your Server is Running!

The FastAPI boilerplate is now running with Docker. Here's how to access it:

### Access the API

- **API Documentation (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **API Base URL:** http://localhost:8000/api

### Quick Commands

```bash
# View running containers
docker compose ps

# View logs
docker compose logs web -f

# Stop containers
docker compose down

# Start containers
docker compose up -d

# Restart web service
docker compose restart web
```

## 🧪 Test the API

### 1. Open Swagger UI
Open your browser and go to: **http://localhost:8000/docs**

### 2. Try Registering a User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "name": "Test User"
  }'
```

### 3. Try Logging In
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### 4. Create a User (via API)
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

## 📊 Container Status

Your containers are running:
- ✅ **PostgreSQL** - Database (port 5432)
- ✅ **Redis** - Cache & Queue (port 6379)
- ✅ **FastAPI Web** - API Server (port 8000)

## 🔧 Next Steps

### 1. Run Database Migrations
```bash
# Connect to web container
docker compose exec web bash

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Exit container
exit
```

### 2. Access PostgreSQL
```bash
docker compose exec postgres psql -U postgres -d fastapi_db
```

### 3. Access Redis CLI
```bash
docker compose exec redis redis-cli
```

## 🐛 Troubleshooting

### Server not starting?
```bash
# Check logs
docker compose logs web -f

# Restart all services
docker compose restart
```

### Database connection issues?
```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Check logs
docker compose logs postgres
```

### Redis issues?
```bash
# Check Redis status
docker compose ps redis
docker compose logs redis
```

## 📝 Environment Variables

Create a `.env` file in the project root:

```bash
cp env.example .env
```

Edit `.env` with your configuration.

## 🎯 Summary

You now have:
- ✅ FastAPI server running on port 8000
- ✅ PostgreSQL database on port 5432
- ✅ Redis on port 6379
- ✅ API documentation at /docs
- ✅ Ready to develop!

## Quick Access Links

- [API Docs](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [Health Check](http://localhost:8000/health)
- [Base API](http://localhost:8000/api)

---

**Happy Coding! 🎉**

