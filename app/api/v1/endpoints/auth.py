"""인증 관련 엔드포인트"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
)
from core.settings import settings

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    사용자 로그인
    
    OAuth2 호환 토큰 로그인, 향후 JWT 토큰 사용 가능
    """
    # 실제로는 데이터베이스에서 사용자 검증
    # 여기서는 예시를 위한 하드코딩
    if form_data.username == "admin" and form_data.password == "admin":
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=form_data.username,
            expires_delta=access_token_expires,
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="잘못된 사용자명 또는 비밀번호",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/register")
async def register(
    username: str,
    password: str,
    email: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    새 사용자 등록
    """
    # 실제로는 데이터베이스에 사용자 생성
    # 여기서는 예시를 위한 간단한 응답
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(password)
    
    # TODO: 데이터베이스에 사용자 저장
    # user = await create_user(db, username, hashed_password, email)
    
    return {
        "message": "사용자가 성공적으로 등록되었습니다",
        "username": username,
        "email": email,
    }


@router.post("/refresh")
async def refresh_token(
    # current_user: str = Depends(get_current_user),
) -> Any:
    """
    토큰 갱신
    """
    # 실제로는 리프레시 토큰을 사용한 토큰 갱신 구현
    return {"message": "토큰 갱신 기능은 추후 구현 예정"}


@router.post("/logout")
async def logout(
    # current_user: str = Depends(get_current_user),
) -> Any:
    """
    사용자 로그아웃
    """
    # 실제로는 토큰 블랙리스트 처리
    return {"message": "성공적으로 로그아웃되었습니다"} 