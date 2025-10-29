from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import auth, users, templates
from app.common.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)
from app.services.cache_service import cache_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await cache_service.connect()
    yield
    await close_db()
    await cache_service.disconnect()



app = FastAPI(
    title="FastAPI Boilerplate",
    description="FastAPI boilerplate with PostgreSQL, Redis, Arq, and JWT",
    version=settings.version,
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token (without 'Bearer ' prefix)",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    return {"message": "FastAPI Boilerplate API"}


@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.version}


app.include_router(auth.router, prefix=f"{settings.prefix}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.prefix}/users", tags=["users"])
app.include_router(
    templates.router, prefix=f"{settings.prefix}/templates", tags=["templates"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )

