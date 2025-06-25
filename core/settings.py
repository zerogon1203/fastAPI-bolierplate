"""Application settings and configuration."""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # 기본 애플리케이션 설정
    APP_NAME: str = "FastAPI 보일러플레이트"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 보안 설정
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 데이터베이스 설정 (모듈식)
    DB_TYPE: str = "postgresql"  # postgresql, mysql, sqlite
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_db"
    DB_USER: str = "username"
    DB_PASSWORD: str = "password"
    DB_SCHEMA: str = "public"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_PRE_PING: bool = True
    DB_ECHO: bool = False
    
    # 테스트 데이터베이스 설정
    TEST_DB_TYPE: str = "postgresql"
    TEST_DB_HOST: str = "localhost"
    TEST_DB_PORT: int = 5432
    TEST_DB_NAME: str = "fastapi_test_db"
    TEST_DB_USER: str = "username"
    TEST_DB_PASSWORD: str = "password"
    
    # SQLite 설정
    SQLITE_DATABASE_PATH: str = "./data/app.db"
    TEST_SQLITE_DATABASE_PATH: str = "./data/test.db"
    
    # Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    
    # AI/LLM 설정
    USE_AI_SERVICE: bool = False
    DEFAULT_PROVIDER: Optional[str] = None
    DEFAULT_LLM_MODEL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    OLLAMA_HOST: Optional[str] = None
    
    # LangSmith 설정
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "fastapi-boilerplate"
    
    # MCP 설정
    MCP_SERVERS_CONFIG_PATH: str = "./config/mcp_servers.json"
    MCP_ENABLED: bool = True
    
    # 벡터 데이터베이스 설정
    PINECONE_API_KEY: Optional[str] = None
    WEAVIATE_URL: Optional[HttpUrl] = None
    CHROMADB_PERSIST_DIRECTORY: str = "./data/chromadb"
    
    # AI 모델 설정
    DEFAULT_LLM_MODEL: str = "gpt-4"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    
    # 파일 시스템 설정
    FILE_STORAGE_TYPE: str = "local"  # local, s3
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # 로컬 스토리지 설정
    LOCAL_UPLOAD_DIR: str = "./uploads"
    LOCAL_STATIC_DIR: str = "./static"
    
    # AWS S3 설정
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-northeast-2"
    S3_BUCKET_NAME: Optional[str] = None
    S3_UPLOAD_PREFIX: str = "uploads/"
    S3_STATIC_PREFIX: str = "static/"
    S3_PUBLIC_READ: bool = True
    S3_ENDPOINT_URL: Optional[str] = None  # MinIO나 다른 S3 호환 서비스용
    
    class Config:
        env_file = [".env.development", ".env"]  # 순서대로 시도
        case_sensitive = True


class DevelopmentSettings(Settings):
    """개발 환경 설정"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env"


class ProductionSettings(Settings):
    """프로덕션 환경 설정"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    
    class Config:
        env_file = ".env.production"


class TestingSettings(Settings):
    """테스트 환경 설정"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    # 테스트용 SQLite 사용
    DB_TYPE: str = "sqlite"
    TEST_DB_TYPE: str = "sqlite"
    SQLITE_DATABASE_PATH: str = "./data/test_app.db"
    TEST_SQLITE_DATABASE_PATH: str = "./data/test.db"
    
    class Config:
        env_file = ".env.testing"


def get_settings() -> Settings:
    """환경에 따른 설정 반환"""
    import os
    
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# 전역 설정 인스턴스
settings = get_settings() 