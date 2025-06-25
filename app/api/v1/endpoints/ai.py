"""AI 관련 엔드포인트"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ai.providers import get_available_providers, get_llm_provider
from app.api.deps import get_current_user_optional, get_db
from core.logging import log_ai_event, log_mcp_event
from core.settings import settings

router = APIRouter()


@router.get("/")
async def get_ai_info(
    current_user: Optional[str] = Depends(get_current_user_optional),
) -> Any:
    """
    AI 정보 조회
    """
    providers = get_available_providers()
    return {
        "providers": providers,
    }


@router.post("/chat")
async def chat_with_ai(
    message: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    current_user: Optional[str] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    AI와 채팅

    Langchain을 사용하여 다양한 LLM 모델과 대화
    """
    # AI 서비스 가용성 확인
    if not (
        settings.OPENAI_API_KEY
        or settings.ANTHROPIC_API_KEY
        or settings.GOOGLE_API_KEY
        or settings.OLLAMA_HOST
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 서비스가 설정되지 않았습니다",
        )
    print(f"settings.DEFAULT_PROVIDER : {settings.DEFAULT_PROVIDER}")
    print(f"settings.DEFAULT_LLM_MODEL : {settings.DEFAULT_LLM_MODEL}")
    print(f"provider : {provider}")
    print(f"model : {model}")
    # 사용할 모델 결정
    selected_model = model or settings.DEFAULT_LLM_MODEL

    provider = provider or settings.DEFAULT_PROVIDER

    print(provider, selected_model)

    llm_provider = get_llm_provider(provider_name=provider, model_name=selected_model)

    # AI 이벤트 로깅
    log_ai_event(
        "chat_request",
        user=current_user,
        provider=provider,
        model=selected_model,
        message_length=len(message),
    )
    response = await llm_provider.chat_completion(
        messages=[{"role": "user", "content": message}]
    )

    log_ai_event(
        "chat_response",
        user=current_user,
        model=selected_model,
        response_length=len(response),
    )

    return {
        "response": response,
        "model": selected_model,
        "usage": {
            "prompt_tokens": len(message.split()),
            "completion_tokens": len(response.split()),
            "total_tokens": len(message.split()) + len(response.split()),
        },
    }


@router.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    analysis_type: str = "summary",
    current_user: Optional[str] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    문서 분석

    업로드된 문서를 AI로 분석 (요약, 키워드 추출 등)
    """
    if not (settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 서비스가 설정되지 않았습니다",
        )

    # 파일 크기 확인
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"파일 크기가 너무 큽니다. 최대 {settings.MAX_FILE_SIZE} bytes",
        )

    # 파일 내용 읽기
    content = await file.read()

    log_ai_event(
        "document_analysis",
        user=current_user,
        file_name=file.filename,
        file_size=len(content),
        analysis_type=analysis_type,
    )

    # 실제로는 문서 처리 및 AI 분석
    analysis_result = f"{file.filename} 파일의 {analysis_type} 분석 결과입니다."

    return {
        "file_name": file.filename,
        "file_size": len(content),
        "analysis_type": analysis_type,
        "result": analysis_result,
        "confidence": 0.95,
    }


@router.post("/search")
async def search_knowledge(
    query: str,
    limit: int = 5,
    current_user: Optional[str] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    지식 베이스 검색

    RAG (Retrieval-Augmented Generation)를 사용한 지식 검색
    """
    if not (settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 서비스가 설정되지 않았습니다",
        )

    log_ai_event("knowledge_search", user=current_user, query=query, limit=limit)

    # 실제로는 벡터 검색 및 RAG 구현
    search_results = [
        {
            "title": f"검색 결과 {i+1}",
            "content": f"'{query}'에 대한 {i+1}번째 검색 결과입니다.",
            "score": 0.9 - (i * 0.1),
            "source": f"document_{i+1}.pdf",
        }
        for i in range(min(limit, 3))
    ]

    return {
        "query": query,
        "results": search_results,
        "total_found": len(search_results),
    }


@router.get("/models")
async def get_available_models() -> Any:
    """
    사용 가능한 AI 모델 목록
    """
    models = []

    if settings.OPENAI_API_KEY:
        models.extend(
            [
                {"provider": "OpenAI", "model": "gpt-4", "type": "chat"},
                {"provider": "OpenAI", "model": "gpt-3.5-turbo", "type": "chat"},
                {
                    "provider": "OpenAI",
                    "model": "text-embedding-ada-002",
                    "type": "embedding",
                },
            ]
        )

    if settings.ANTHROPIC_API_KEY:
        models.extend(
            [
                {"provider": "Anthropic", "model": "claude-3-opus", "type": "chat"},
                {"provider": "Anthropic", "model": "claude-3-sonnet", "type": "chat"},
            ]
        )

    return {
        "available_models": models,
        "default_model": settings.DEFAULT_LLM_MODEL,
        "total_models": len(models),
    }


@router.get("/mcp/servers")
async def get_mcp_servers(
    current_user: Optional[str] = Depends(get_current_user_optional),
) -> Any:
    """
    MCP 서버 목록 조회
    """
    if not settings.MCP_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MCP 서비스가 비활성화되어 있습니다",
        )

    log_mcp_event("list_servers", user=current_user)

    # 실제로는 MCP 서버 설정 파일 읽기
    return {
        "mcp_enabled": settings.MCP_ENABLED,
        "config_path": settings.MCP_SERVERS_CONFIG_PATH,
        "servers": [
            {"name": "filesystem", "status": "available"},
            {"name": "brave-search", "status": "available"},
            {"name": "github", "status": "available"},
        ],
    }


@router.post("/mcp/call-tool")
async def call_mcp_tool(
    server: str,
    tool: str,
    arguments: dict,
    current_user: Optional[str] = Depends(get_current_user_optional),
) -> Any:
    """
    MCP 도구 호출
    """
    if not settings.MCP_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MCP 서비스가 비활성화되어 있습니다",
        )

    log_mcp_event(
        "tool_call", user=current_user, server=server, tool=tool, arguments=arguments
    )

    # 실제로는 MCP 클라이언트를 사용한 도구 호출
    result = f"MCP 서버 '{server}'의 도구 '{tool}' 호출 결과"

    return {
        "server": server,
        "tool": tool,
        "arguments": arguments,
        "result": result,
        "success": True,
    }
