"""Application settings and configuration."""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


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

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 데이터베이스 설정
    DATABASE_URL: Optional[PostgresDsn] = None
    TEST_DATABASE_URL: Optional[PostgresDsn] = None
    
    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI/LLM 설정
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
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
    
    # 파일 업로드 설정
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentSettings(Settings):
    """개발 환경 설정"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env.development"


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
    
    # 테스트용 인메모리 데이터베이스
    DATABASE_URL: Optional[PostgresDsn] = "postgresql://test:test@localhost/test_db"
    
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