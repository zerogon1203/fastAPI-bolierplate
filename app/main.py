"""FastAPI 애플리케이션 메인 진입점"""

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from core.settings import settings
from core.database import create_tables, check_db_connection
from core.logging import log_request, log_response
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시
    logger.info("🚀 FastAPI 애플리케이션 시작")
    
    # 데이터베이스 연결 확인
    if await check_db_connection():
        logger.info("✅ 데이터베이스 연결 성공")
        
        # 개발 환경에서만 테이블 자동 생성
        if settings.DEBUG:
            await create_tables()
            logger.info("📋 데이터베이스 테이블 생성 완료")
    else:
        logger.warning("⚠️ 데이터베이스 연결 실패 - 데이터베이스 없이 실행")
    
    # AI 서비스 초기화
    if settings.MCP_ENABLED:
        logger.info("🤖 MCP 서비스 초기화")
    
    if settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY:
        logger.info("🧠 AI 서비스 사용 가능")
    
    yield
    
    # 종료 시
    logger.info("🛑 FastAPI 애플리케이션 종료")


# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 시대를 위한 FastAPI 보일러플레이트 (Langchain + MCP 지원)",
    openapi_url="/api/v1/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# 신뢰할 수 있는 호스트 설정 (프로덕션)
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
    )

# CORS 미들웨어
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """요청/응답 로깅 미들웨어"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # 요청 로깅
    log_request(
        request_id=request_id,
        method=request.method,
        url=request.url,
        user_agent=request.headers.get("user-agent"),
        client_ip=request.client.host if request.client else None,
    )
    
    # 요청 처리
    try:
        response = await call_next(request)
        
        # 응답 로깅
        process_time = time.time() - start_time
        log_response(
            request_id=request_id,
            status_code=response.status_code,
            duration=process_time,
        )
        
        # 응답 헤더에 요청 ID 추가
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        # 에러 로깅
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {str(e)}",
            request_id=request_id,
            error=str(e),
            duration=process_time,
        )
        
        # 에러 응답
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request_id},
            headers={"X-Request-ID": request_id},
        )


# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    db_status = await check_db_connection()
    
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if db_status else "disconnected",
        "ai_enabled": bool(settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY),
        "mcp_enabled": settings.MCP_ENABLED,
    }


# 메트릭 엔드포인트 (프로덕션에서는 인증 필요)
@app.get("/metrics")
async def metrics():
    """메트릭 엔드포인트"""
    if not settings.DEBUG:
        return {"detail": "Metrics endpoint disabled in production"}
    
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
    }


# API 라우터 포함
app.include_router(api_router, prefix="/api/v1")


# 루트 엔드포인트
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}",
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health",
        "api": "/api/v1",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    ) 