"""AI/LLM 통합 모듈

이 모듈은 다양한 AI 기능들을 제공합니다:
- Langchain 체인 및 에이전트
- 다중 LLM 프로바이더 지원
- MCP (Model Context Protocol) 통합
- 벡터 임베딩 및 검색
- 프롬프트 템플릿 관리
"""

from .providers import get_llm_provider, get_embedding_provider, get_available_providers
from .chains import get_chat_chain
# from .tools import get_available_tools  # TODO: tools 모듈 구현 필요
from .prompts import PromptManager

__all__ = [
    "get_llm_provider",
    "get_embedding_provider", 
    "get_chat_chain",
    "get_available_providers"
    # "get_rag_chain",
    # "get_available_tools",  # TODO: tools 모듈 구현 후 주석 해제
    "PromptManager",
] 