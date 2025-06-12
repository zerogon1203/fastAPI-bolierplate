"""사용자 모델 정의"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    """사용자 모델"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # 사용자 상태
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # 프로필 정보
    profile_image = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # 설정
    language = Column(String(10), default="ko")
    timezone = Column(String(50), default="Asia/Seoul")
    
    # AI 관련 설정
    preferred_ai_model = Column(String(100), default="gpt-4")
    ai_conversation_limit = Column(Integer, default=100)
    
    # 메타 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


# Pydantic 모델들 (API 요청/응답용)
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """사용자 생성 요청 모델"""
    
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    language: str = "ko"
    timezone: str = "Asia/Seoul"


class UserUpdate(BaseModel):
    """사용자 정보 수정 요청 모델"""
    
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    preferred_ai_model: Optional[str] = None
    profile_image: Optional[str] = None


class UserResponse(BaseModel):
    """사용자 정보 응답 모델"""
    
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    profile_image: Optional[str]
    bio: Optional[str]
    language: str
    timezone: str
    preferred_ai_model: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """로그인 요청 모델"""
    
    username: str  # email 또는 username
    password: str