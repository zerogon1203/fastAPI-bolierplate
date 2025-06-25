"""API v1 메인 라우터"""

from fastapi import APIRouter

from app.api.v1.endpoints import ai, auth, health, users

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(auth.router, prefix="/auth", tags=["인증"])

# 사용자 관련 엔드포인트
api_router.include_router(users.router, prefix="/users", tags=["사용자"])

# 헬스체크 엔드포인트
api_router.include_router(health.router, prefix="/health", tags=["헬스체크"])

# AI 관련 엔드포인트
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
