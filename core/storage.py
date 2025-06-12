"""파일 스토리지 관리 모듈"""

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional, Tuple
from urllib.parse import urljoin

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, UploadFile

from core.settings import settings


class StorageBackend(ABC):
    """스토리지 백엔드 추상 클래스"""
    
    @abstractmethod
    async def save_file(
        self, 
        file: UploadFile, 
        filename: str, 
        folder: str = ""
    ) -> str:
        """파일 저장"""
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """파일 삭제"""
        pass
    
    @abstractmethod
    async def get_file_url(self, file_path: str) -> str:
        """파일 URL 반환"""
        pass
    
    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """파일 존재 여부 확인"""
        pass


class LocalStorageBackend(StorageBackend):
    """로컬 파일 시스템 백엔드"""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_file(
        self, 
        file: UploadFile, 
        filename: str, 
        folder: str = ""
    ) -> str:
        """로컬에 파일 저장"""
        # 폴더 생성
        if folder:
            folder_path = self.base_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = folder_path / filename
        else:
            file_path = self.base_dir / filename
        
        try:
            # 파일 저장
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 상대 경로 반환
            relative_path = str(file_path.relative_to(self.base_dir))
            return relative_path
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"파일 저장 실패: {str(e)}"
            )
    
    async def delete_file(self, file_path: str) -> bool:
        """로컬 파일 삭제"""
        try:
            full_path = self.base_dir / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    async def get_file_url(self, file_path: str) -> str:
        """로컬 파일 URL 반환"""
        # 정적 파일 서빙 URL 반환
        return f"/static/{file_path}"
    
    async def file_exists(self, file_path: str) -> bool:
        """파일 존재 여부 확인"""
        full_path = self.base_dir / file_path
        return full_path.exists()


class S3StorageBackend(StorageBackend):
    """AWS S3 스토리지 백엔드"""
    
    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
        endpoint_url: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                endpoint_url=endpoint_url
            )
            
            # 버킷 존재 여부 확인
            self.s3_client.head_bucket(Bucket=bucket_name)
            
        except NoCredentialsError:
            raise HTTPException(
                status_code=500,
                detail="AWS 인증 정보가 없습니다."
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                raise HTTPException(
                    status_code=500,
                    detail=f"S3 버킷 '{bucket_name}'을 찾을 수 없습니다."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"S3 연결 실패: {str(e)}"
                )
    
    async def save_file(
        self, 
        file: UploadFile, 
        filename: str, 
        folder: str = ""
    ) -> str:
        """S3에 파일 업로드"""
        try:
            # S3 키 생성
            if folder:
                s3_key = f"{folder}/{filename}"
            else:
                s3_key = filename
            
            # 파일 업로드
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': file.content_type or 'application/octet-stream',
                    'ACL': 'public-read' if settings.S3_PUBLIC_READ else 'private'
                }
            )
            
            return s3_key
            
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"S3 업로드 실패: {str(e)}"
            )
    
    async def delete_file(self, file_path: str) -> bool:
        """S3 파일 삭제"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError:
            return False
    
    async def get_file_url(self, file_path: str) -> str:
        """S3 파일 URL 반환"""
        if settings.S3_PUBLIC_READ:
            # 공개 URL 반환
            if settings.S3_ENDPOINT_URL:
                return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{file_path}"
            else:
                return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_path}"
        else:
            # 서명된 URL 생성 (1시간 유효)
            try:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': file_path},
                    ExpiresIn=3600
                )
                return url
            except ClientError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"URL 생성 실패: {str(e)}"
                )
    
    async def file_exists(self, file_path: str) -> bool:
        """S3 파일 존재 여부 확인"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_path)
            return True
        except ClientError:
            return False


class FileStorageManager:
    """파일 스토리지 관리자"""
    
    def __init__(self):
        self.backend = self._get_backend()
    
    def _get_backend(self) -> StorageBackend:
        """설정에 따른 스토리지 백엔드 반환"""
        if settings.FILE_STORAGE_TYPE.lower() == "s3":
            if not all([
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY,
                settings.S3_BUCKET_NAME
            ]):
                raise ValueError("S3 설정이 불완전합니다. AWS 인증 정보와 버킷명을 확인하세요.")
            
            return S3StorageBackend(
                bucket_name=settings.S3_BUCKET_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
                endpoint_url=settings.S3_ENDPOINT_URL
            )
        
        elif settings.FILE_STORAGE_TYPE.lower() == "local":
            return LocalStorageBackend(settings.LOCAL_UPLOAD_DIR)
        
        else:
            raise ValueError(f"지원하지 않는 스토리지 타입: {settings.FILE_STORAGE_TYPE}")
    
    async def save_upload_file(
        self, 
        file: UploadFile, 
        filename: Optional[str] = None,
        folder: str = ""
    ) -> Tuple[str, str]:
        """업로드된 파일 저장"""
        # 파일 크기 검사
        file.file.seek(0, 2)  # 파일 끝으로 이동
        file_size = file.file.tell()
        file.file.seek(0)  # 파일 시작으로 복귀
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"파일 크기가 제한을 초과했습니다. 최대 {settings.MAX_FILE_SIZE} bytes"
            )
        
        # 파일명 생성
        if not filename:
            filename = file.filename or "unknown"
        
        # 안전한 파일명으로 변환
        safe_filename = self._make_safe_filename(filename)
        
        # 파일 저장
        file_path = await self.backend.save_file(file, safe_filename, folder)
        file_url = await self.backend.get_file_url(file_path)
        
        return file_path, file_url
    
    async def delete_file(self, file_path: str) -> bool:
        """파일 삭제"""
        return await self.backend.delete_file(file_path)
    
    async def get_file_url(self, file_path: str) -> str:
        """파일 URL 반환"""
        return await self.backend.get_file_url(file_path)
    
    async def file_exists(self, file_path: str) -> bool:
        """파일 존재 여부 확인"""
        return await self.backend.file_exists(file_path)
    
    def _make_safe_filename(self, filename: str) -> str:
        """안전한 파일명 생성"""
        import re
        import uuid
        from datetime import datetime
        
        # 파일명과 확장자 분리
        name, ext = os.path.splitext(filename)
        
        # 안전하지 않은 문자 제거
        safe_name = re.sub(r'[^\w\-_.]', '_', name)
        
        # 타임스탬프와 UUID 추가로 중복 방지
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        return f"{safe_name}_{timestamp}_{unique_id}{ext}"


# 전역 파일 스토리지 관리자 인스턴스
storage_manager = FileStorageManager() 