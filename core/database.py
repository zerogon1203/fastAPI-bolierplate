"""Database configuration and session management."""

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


def init_db():
    """데이터베이스 초기화"""
    global engine, SessionLocal, async_engine, AsyncSessionLocal
    
    if settings.DATABASE_URL:
        # 동기 엔진 설정
        sync_database_url = str(settings.DATABASE_URL).replace(
            "postgresql+asyncpg://", "postgresql://"
        )
        engine = create_engine(
            sync_database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        # 비동기 엔진 설정
        async_database_url = str(settings.DATABASE_URL)
        if not async_database_url.startswith("postgresql+asyncpg://"):
            async_database_url = async_database_url.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
        
        async_engine = create_async_engine(
            async_database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        
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