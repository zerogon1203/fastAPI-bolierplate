"""Database configuration and session management."""

from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.settings import settings

# 동기 엔진 및 세션
engine = None
SessionLocal = None

# 비동기 엔진 및 세션
async_engine = None
AsyncSessionLocal = None

# Base 클래스
Base = declarative_base()


def build_database_url(
    db_type: str,
    host: str,
    port: int,
    name: str,
    user: str,
    password: str,
    is_async: bool = False,
    sqlite_path: Optional[str] = None
) -> str:
    """데이터베이스 URL 생성"""
    if db_type.lower() == "sqlite":
        if sqlite_path:
            return f"sqlite{'aiosqlite' if is_async else ''}:///{sqlite_path}"
        else:
            raise ValueError("SQLite requires database path")
    
    elif db_type.lower() == "postgresql":
        driver = "postgresql+asyncpg" if is_async else "postgresql"
        return f"{driver}://{user}:{password}@{host}:{port}/{name}"
    
    elif db_type.lower() == "mysql":
        driver = "mysql+aiomysql" if is_async else "mysql+pymysql"
        return f"{driver}://{user}:{password}@{host}:{port}/{name}"
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_database_urls():
    """운영 및 테스트 데이터베이스 URL 반환"""
    # 운영 데이터베이스 URL
    if settings.DB_TYPE.lower() == "sqlite":
        database_url = build_database_url(
            settings.DB_TYPE,
            None, None, None, None, None,
            is_async=False,
            sqlite_path=settings.SQLITE_DATABASE_PATH
        )
        async_database_url = build_database_url(
            settings.DB_TYPE,
            None, None, None, None, None,
            is_async=True,
            sqlite_path=settings.SQLITE_DATABASE_PATH
        )
    else:
        database_url = build_database_url(
            settings.DB_TYPE,
            settings.DB_HOST,
            settings.DB_PORT,
            settings.DB_NAME,
            settings.DB_USER,
            settings.DB_PASSWORD,
            is_async=False
        )
        async_database_url = build_database_url(
            settings.DB_TYPE,
            settings.DB_HOST,
            settings.DB_PORT,
            settings.DB_NAME,
            settings.DB_USER,
            settings.DB_PASSWORD,
            is_async=True
        )
    
    # 테스트 데이터베이스 URL
    if settings.TEST_DB_TYPE.lower() == "sqlite":
        test_database_url = build_database_url(
            settings.TEST_DB_TYPE,
            None, None, None, None, None,
            is_async=False,
            sqlite_path=settings.TEST_SQLITE_DATABASE_PATH
        )
        test_async_database_url = build_database_url(
            settings.TEST_DB_TYPE,
            None, None, None, None, None,
            is_async=True,
            sqlite_path=settings.TEST_SQLITE_DATABASE_PATH
        )
    else:
        test_database_url = build_database_url(
            settings.TEST_DB_TYPE,
            settings.TEST_DB_HOST,
            settings.TEST_DB_PORT,
            settings.TEST_DB_NAME,
            settings.TEST_DB_USER,
            settings.TEST_DB_PASSWORD,
            is_async=False
        )
        test_async_database_url = build_database_url(
            settings.TEST_DB_TYPE,
            settings.TEST_DB_HOST,
            settings.TEST_DB_PORT,
            settings.TEST_DB_NAME,
            settings.TEST_DB_USER,
            settings.TEST_DB_PASSWORD,
            is_async=True
        )
    
    return database_url, async_database_url, test_database_url, test_async_database_url


def init_db():
    """데이터베이스 초기화"""
    global engine, SessionLocal, async_engine, AsyncSessionLocal
    
    database_url, async_database_url, _, _ = get_database_urls()
    
    # 동기 엔진 설정
    engine_kwargs = {
        "echo": settings.DB_ECHO,
    }
    
    # SQLite가 아닌 경우에만 커넥션 풀 설정
    if settings.DB_TYPE.lower() != "sqlite":
        engine_kwargs.update({
            "pool_pre_ping": settings.DB_POOL_PRE_PING,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
        })
    
    engine = create_engine(database_url, **engine_kwargs)
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # 비동기 엔진 설정
    async_engine_kwargs = {
        "echo": settings.DB_ECHO,
    }
    
    if settings.DB_TYPE.lower() != "sqlite":
        async_engine_kwargs.update({
            "pool_pre_ping": settings.DB_POOL_PRE_PING,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
        })
    
    async_engine = create_async_engine(async_database_url, **async_engine_kwargs)
    
    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )


def get_db():
    """동기 데이터베이스 세션 의존성"""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """비동기 데이터베이스 세션 의존성"""
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database not initialized. Call init_db() first.")
    
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    """테이블 생성 (개발용)"""
    if async_engine is None:
        raise RuntimeError("Async database not initialized. Call init_db() first.")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """테이블 삭제 (테스트용)"""
    if async_engine is None:
        raise RuntimeError("Async database not initialized. Call init_db() first.")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def check_db_connection():
    """데이터베이스 연결 상태 확인"""
    try:
        if AsyncSessionLocal is None:
            return False
        
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False


# 데이터베이스 초기화
init_db() 