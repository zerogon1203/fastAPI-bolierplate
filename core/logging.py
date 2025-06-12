"""Logging configuration using Loguru."""

import sys
import json
from pathlib import Path
from typing import Dict, Any

from loguru import logger

from core.settings import settings


def serialize_record(record: Dict[str, Any]) -> str:
    """로그 레코드를 JSON 형태로 직렬화"""
    subset = {
        "timestamp": record["time"].timestamp(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
    }
    
    # 추가 필드가 있으면 포함
    if record.get("extra"):
        subset.update(record["extra"])
    
    return json.dumps(subset, ensure_ascii=False)


def setup_logging():
    """로깅 설정 초기화"""
    # 기본 핸들러 제거
    logger.remove()
    
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 콘솔 로깅 (개발환경)
    if settings.DEBUG:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            colorize=True,
        )
    
    # 파일 로깅 (JSON 형태)
    logger.add(
        log_dir / "app.log",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="30 days",
        compression="gz",
    )
    
    # 에러 전용 로깅
    logger.add(
        log_dir / "error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 week",
        retention="3 months",
        compression="gz",
    )
    
    # AI 관련 로깅
    logger.add(
        log_dir / "ai.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="7 days",
        filter=lambda record: "ai" in record.get("extra", {}),
    )
    
    # MCP 관련 로깅
    logger.add(
        log_dir / "mcp.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="7 days",
        filter=lambda record: "mcp" in record.get("extra", {}),
    )


def get_logger(name: str) -> logger:
    """이름을 가진 로거 반환"""
    return logger.bind(name=name)


def log_ai_event(event_type: str, **kwargs):
    """AI 관련 이벤트 로깅"""
    logger.bind(ai=True).info(
        f"AI Event: {event_type}",
        event_type=event_type,
        **kwargs
    )


def log_mcp_event(event_type: str, **kwargs):
    """MCP 관련 이벤트 로깅"""
    logger.bind(mcp=True).info(
        f"MCP Event: {event_type}",
        event_type=event_type,
        **kwargs
    )


def log_request(request_id: str, method: str, url: str, **kwargs):
    """HTTP 요청 로깅"""
    logger.info(
        f"Request: {method} {url}",
        request_id=request_id,
        method=method,
        url=str(url),
        **kwargs
    )


def log_response(request_id: str, status_code: int, duration: float, **kwargs):
    """HTTP 응답 로깅"""
    logger.info(
        f"Response: {status_code} ({duration:.3f}s)",
        request_id=request_id,
        status_code=status_code,
        duration=duration,
        **kwargs
    )


# 로깅 설정 초기화
setup_logging() 