"""API 의존성 주입 함수들"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_db
from core.security import create_credentials_exception, verify_token

# Bearer 토큰 보안 스키마
security = HTTPBearer()


async def get_db() -> AsyncSession:
    """비동기 데이터베이스 세션 의존성"""
    async for session in get_async_db():
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """현재 사용자 인증 의존성"""
    token = credentials.credentials
    subject = verify_token(token)

    if subject is None:
        raise create_credentials_exception()

    return subject


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[str]:
    """선택적 사용자 인증 의존성 (토큰이 없어도 됨)"""
    if not credentials:
        return None

    token = credentials.credentials
    return verify_token(token)


async def get_current_active_user(
    current_user: str = Depends(get_current_user),
) -> str:
    """활성 사용자 의존성"""
    # 여기에 사용자가 활성 상태인지 확인하는 로직 추가
    # 예: 데이터베이스에서 사용자 상태 확인
    return current_user


def require_roles(*required_roles: str):
    """특정 역할을 요구하는 의존성 팩토리"""

    async def check_roles(
        current_user: str = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> str:
        # 여기에 사용자 역할 확인 로직 추가
        # 예: 데이터베이스에서 사용자 역할 조회
        user_roles = []  # 실제로는 DB에서 조회

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )

        return current_user

    return check_roles


def require_admin():
    """관리자 권한 요구 의존성"""
    return require_roles("admin")


def require_moderator():
    """모더레이터 권한 요구 의존성"""
    return require_roles("admin", "moderator")
