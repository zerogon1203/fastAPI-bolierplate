"""프로바이더 팩토리 함수들"""

from typing import Optional
from .base import BaseLLMProvider, BaseEmbeddingProvider
from .openai_provider import OpenAIProvider, OpenAIEmbeddingProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .ollama_provider import OllamaProvider
from core.settings import settings


def get_llm_provider(
    provider_name: str = None,
    api_key: str = None,
    model_name: str = None,
    **kwargs
) -> BaseLLMProvider:
    """LLM 프로바이더 인스턴스 반환
    
    Args:
        provider_name: 프로바이더 이름 (openai, anthropic, google, ollama)
        api_key: API 키
        model_name: 모델 이름
        **kwargs: 추가 설정
    """
    provider_name = provider_name or settings.DEFAULT_PROVIDER or "openai"
    
    if provider_name.lower() == "openai":
        return OpenAIProvider(api_key=api_key, model_name=model_name, **kwargs)
    elif provider_name.lower() == "anthropic":
        return AnthropicProvider(api_key=api_key, model_name=model_name, **kwargs)
    elif provider_name.lower() == "google":
        return GoogleProvider(api_key=api_key, model_name=model_name, **kwargs)
    elif provider_name.lower() == "ollama":
        return OllamaProvider(model_name=model_name, **kwargs)
    else:
        raise ValueError(f"지원하지 않는 프로바이더: {provider_name}")


def get_embedding_provider(
    provider_name: str = None,
    api_key: str = None,
    model_name: str = None,
    **kwargs
) -> BaseEmbeddingProvider:
    """임베딩 프로바이더 인스턴스 반환
    
    Args:
        provider_name: 프로바이더 이름 (현재는 openai만 지원)
        api_key: API 키
        model_name: 모델 이름
        **kwargs: 추가 설정
    """
    provider_name = provider_name or "openai"
    
    if provider_name.lower() == "openai":
        return OpenAIEmbeddingProvider(api_key=api_key, model_name=model_name, **kwargs)
    else:
        raise ValueError(f"지원하지 않는 임베딩 프로바이더: {provider_name}")


def get_available_providers() -> dict:
    """사용 가능한 프로바이더 정보 반환"""
    providers = {}
    
    # OpenAI 확인
    if settings.OPENAI_API_KEY:
        openai_provider = OpenAIProvider()
        providers["openai"] = {
            "name": "OpenAI",
            "models": openai_provider.available_models,
            "embedding_models": OpenAIEmbeddingProvider().available_models
        }
    
    # Anthropic 확인
    if settings.ANTHROPIC_API_KEY:
        anthropic_provider = AnthropicProvider()
        providers["anthropic"] = {
            "name": "Anthropic",
            "models": anthropic_provider.available_models
        }
    
    # Google 확인
    if settings.GOOGLE_API_KEY:
        google_provider = GoogleProvider()
        providers["google"] = {
            "name": "Google",
            "models": google_provider.available_models
        }
    if settings.OLLAMA_HOST:
        ollama_provider = OllamaProvider()
        providers["ollama"] = {
            "name": "Ollama",
            "models": ollama_provider.available_models
        }
    
    return providers 