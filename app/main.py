from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import auth, users, templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="FastAPI Boilerplate",
    description="FastAPI boilerplate with PostgreSQL, Redis, Arq, and JWT",
    version=settings.version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

