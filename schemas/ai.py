"""AI 관련 Pydantic 스키마"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """채팅 메시지 스키마"""
    
    role: str = Field(..., description="메시지 역할 (user, assistant, system)")
    content: str = Field(..., description="메시지 내용")
    timestamp: Optional[datetime] = Field(None, description="메시지 시간")


class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    
    message: str = Field(..., description="사용자 메시지")
    provider: str = Field(default="openai", description="AI 프로바이더")
    model: Optional[str] = Field(None, description="AI 모델명")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="응답 창의성")
    max_tokens: Optional[int] = Field(None, gt=0, description="최대 토큰 수")
    stream: bool = Field(False, description="스트리밍 여부")
    conversation_id: Optional[str] = Field(None, description="대화 ID")
    system_message: Optional[str] = Field(None, description="시스템 메시지")


class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    
    message: str = Field(..., description="AI 응답 메시지")
    provider: str = Field(..., description="사용된 AI 프로바이더")
    model: str = Field(..., description="사용된 AI 모델")
    conversation_id: str = Field(..., description="대화 ID")
    tokens_used: Optional[int] = Field(None, description="사용된 토큰 수")
    response_time: float = Field(..., description="응답 시간(초)")
    timestamp: datetime = Field(..., description="응답 시간")


class DocumentAnalysisRequest(BaseModel):
    """문서 분석 요청 스키마"""
    
    analysis_type: str = Field(..., description="분석 유형 (summary, keywords, sentiment)")
    language: str = Field(default="ko", description="분석 언어")
    provider: str = Field(default="openai", description="AI 프로바이더")
    detailed: bool = Field(False, description="상세 분석 여부")


class DocumentAnalysisResponse(BaseModel):
    """문서 분석 응답 스키마"""
    
    file_name: str = Field(..., description="파일명")
    analysis_type: str = Field(..., description="분석 유형")
    summary: Optional[str] = Field(None, description="요약")
    keywords: Optional[List[str]] = Field(None, description="키워드")
    sentiment: Optional[str] = Field(None, description="감정 분석")
    language: str = Field(..., description="분석 언어")
    confidence: float = Field(..., description="분석 신뢰도")
    processing_time: float = Field(..., description="처리 시간(초)")


class KnowledgeSearchRequest(BaseModel):
    """지식 검색 요청 스키마"""
    
    query: str = Field(..., description="검색 쿼리")
    top_k: int = Field(5, ge=1, le=20, description="검색 결과 수")
    threshold: float = Field(0.7, ge=0.0, le=1.0, description="유사도 임계값")
    provider: str = Field(default="openai", description="AI 프로바이더")
    include_metadata: bool = Field(True, description="메타데이터 포함 여부")


class KnowledgeSearchResponse(BaseModel):
    """지식 검색 응답 스키마"""
    
    query: str = Field(..., description="검색 쿼리")
    results: List[Dict[str, Any]] = Field(..., description="검색 결과")
    total_results: int = Field(..., description="전체 결과 수")
    search_time: float = Field(..., description="검색 시간(초)")


class AIModel(BaseModel):
    """AI 모델 정보 스키마"""
    
    name: str = Field(..., description="모델명")
    provider: str = Field(..., description="프로바이더")
    description: str = Field(..., description="모델 설명")
    max_tokens: int = Field(..., description="최대 토큰 수")
    supports_streaming: bool = Field(..., description="스트리밍 지원 여부")
    cost_per_1k_tokens: Optional[float] = Field(None, description="1K 토큰당 비용")


class AIProvider(BaseModel):
    """AI 프로바이더 정보 스키마"""
    
    name: str = Field(..., description="프로바이더명")
    display_name: str = Field(..., description="표시명")
    models: List[AIModel] = Field(..., description="사용 가능한 모델 목록")
    is_available: bool = Field(..., description="사용 가능 여부")
    api_key_configured: bool = Field(..., description="API 키 설정 여부")


class MCPToolCall(BaseModel):
    """MCP 도구 호출 스키마"""
    
    tool_name: str = Field(..., description="도구명")
    parameters: Dict[str, Any] = Field(..., description="도구 매개변수")
    server_name: Optional[str] = Field(None, description="MCP 서버명")


class MCPToolResponse(BaseModel):
    """MCP 도구 응답 스키마"""
    
    tool_name: str = Field(..., description="도구명")
    result: Any = Field(..., description="실행 결과")
    success: bool = Field(..., description="실행 성공 여부")
    error_message: Optional[str] = Field(None, description="오류 메시지")
    execution_time: float = Field(..., description="실행 시간(초)")


class EmbeddingRequest(BaseModel):
    """임베딩 요청 스키마"""
    
    text: str = Field(..., description="임베딩할 텍스트")
    provider: str = Field(default="openai", description="임베딩 프로바이더")
    model: Optional[str] = Field(None, description="임베딩 모델")


class EmbeddingResponse(BaseModel):
    """임베딩 응답 스키마"""
    
    embedding: List[float] = Field(..., description="임베딩 벡터")
    dimension: int = Field(..., description="벡터 차원")
    provider: str = Field(..., description="사용된 프로바이더")
    model: str = Field(..., description="사용된 모델")
    processing_time: float = Field(..., description="처리 시간(초)") 