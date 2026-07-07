"""Application configuration management."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "BioNexus AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:5173"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:19000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Database
    database_url: str = "postgresql://biouser:biopass@localhost:5432/bionexus_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_pre_ping: bool = True
    database_echo: bool = False

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Email
    mail_server: str = "smtp.gmail.com"
    mail_port: int = 587
    mail_use_tls: bool = True
    mail_username: str = "your-email@example.com"
    mail_password: str = "your-password"
    mail_from_name: str = "BioNexus AI"
    mail_from_email: str = "noreply@bionexus-ai.com"

    # File Storage
    storage_type: str = "local"
    storage_path: str = "./storage"

    # Encryption
    encryption_key: str = "change-me-in-production"

    # AI/LLM
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000

    # Features
    feature_ai_enabled: bool = True
    feature_research_module_enabled: bool = True
    feature_public_health_module_enabled: bool = True

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 60

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
