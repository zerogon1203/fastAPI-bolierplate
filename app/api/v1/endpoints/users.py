"""사용자 관련 엔드포인트"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_current_user, get_db

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    current_user: str = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    현재 사용자 정보 조회
    """
    # 실제로는 데이터베이스에서 사용자 정보 조회
    return {
        "username": current_user,
        "email": f"{current_user}@example.com",
        "is_active": True,
        "roles": ["user"],
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.put("/me")
async def update_current_user(
    email: str = None,
    full_name: str = None,
    current_user: str = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    현재 사용자 정보 수정
    """
    # 실제로는 데이터베이스에서 사용자 정보 업데이트
    updates = {}
    if email:
        updates["email"] = email
    if full_name:
        updates["full_name"] = full_name

    return {
        "message": "사용자 정보가 업데이트되었습니다",
        "username": current_user,
        "updates": updates,
    }


@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    사용자 목록 조회 (관리자 권한 필요)
    """
    # 실제로는 권한 확인 후 데이터베이스에서 사용자 목록 조회
    return {
        "users": [
            {
                "username": "admin",
                "email": "admin@example.com",
                "is_active": True,
                "roles": ["admin"],
            },
            {
                "username": "user1",
                "email": "user1@example.com",
                "is_active": True,
                "roles": ["user"],
            },
        ],
        "total": 2,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{username}")
async def get_user_by_username(
    username: str,
    current_user: str = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    특정 사용자 정보 조회
    """
    # 실제로는 데이터베이스에서 사용자 조회
    if username == "admin":
        return {
            "username": "admin",
            "email": "admin@example.com",
            "is_active": True,
            "roles": ["admin"],
            "created_at": "2024-01-01T00:00:00Z",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="사용자를 찾을 수 없습니다",
    )


@router.delete("/{username}")
async def delete_user(
    username: str,
    current_user: str = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    사용자 삭제 (관리자 권한 필요)
    """
    # 실제로는 권한 확인 후 데이터베이스에서 사용자 삭제
    if username == current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자기 자신은 삭제할 수 없습니다",
        )

    return {"message": f"사용자 '{username}'이 삭제되었습니다"}
