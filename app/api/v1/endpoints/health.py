"""헬스체크 관련 엔드포인트"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from core.database import check_db_connection
from core.settings import settings

router = APIRouter()


@router.get("/")
async def basic_health_check() -> Any:
    """
    기본 헬스체크
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    상세 헬스체크 (데이터베이스, 외부 서비스 포함)
    """
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": "2024-01-01T00:00:00Z",  # 실제로는 현재 시간
        "checks": {}
    }
    
    # 데이터베이스 연결 확인
    try:
        db_healthy = await check_db_connection()
        health_status["checks"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": "Database connection successful" if db_healthy else "Database connection failed"
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database check failed: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # AI 서비스 확인
    ai_services = []
    if settings.OPENAI_API_KEY:
        ai_services.append("OpenAI")
    if settings.ANTHROPIC_API_KEY:
        ai_services.append("Anthropic")
    if settings.GOOGLE_API_KEY:
        ai_services.append("Google")
    
    health_status["checks"]["ai_services"] = {
        "status": "configured" if ai_services else "not_configured",
        "available_services": ai_services,
        "message": f"{len(ai_services)} AI service(s) configured"
    }
    
    # MCP 서비스 확인
    health_status["checks"]["mcp"] = {
        "status": "enabled" if settings.MCP_ENABLED else "disabled",
        "config_path": settings.MCP_SERVERS_CONFIG_PATH if settings.MCP_ENABLED else None,
        "message": "MCP service is enabled" if settings.MCP_ENABLED else "MCP service is disabled"
    }
    
    # Redis 연결 확인 (향후 구현)
    health_status["checks"]["redis"] = {
        "status": "not_implemented",
        "message": "Redis health check not implemented yet"
    }
    
    return health_status


@router.get("/ready")
async def readiness_check() -> Any:
    """
    준비 상태 확인 (Kubernetes readiness probe 용)
    """
    # 기본적인 준비 상태 확인
    # 데이터베이스 연결, 필수 설정 등 확인
    
    db_ready = await check_db_connection()
    
    if not db_ready and settings.DATABASE_URL:
        return {
            "status": "not_ready",
            "message": "Database connection required but not available"
        }
    
    return {
        "status": "ready",
        "message": "Service is ready to handle requests"
    }


@router.get("/live")
async def liveness_check() -> Any:
    """
    생존 상태 확인 (Kubernetes liveness probe 용)
    """
    return {
        "status": "alive",
        "message": "Service is alive and running"
    } 