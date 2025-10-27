from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    host: str = "localhost"
    port: int = 8000
    environment: str = "development"
    version: str = "0.1.0"
    prefix: str = "/api"

    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi_db"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    jwt_secret_key: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    aes_key: str = "your-aes-key-16"

    smtp_host: str = "smtp.mailtrap.io"
    smtp_port: int = 2525
    smtp_username: str = "username"
    smtp_password: str = "password"
    smtp_from_email: str = "noreply@example.com"
    smtp_from_name: str = "FastAPI Boilerplate"

    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    arq_redis_url: str = "redis://localhost:6379/1"

    log_level: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

