"""OpenAI 프로바이더 구현"""

from typing import AsyncIterator, Dict, List
from langchain_ollama import ChatOllama
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from .base import BaseLLMProvider, BaseEmbeddingProvider
from core.settings import settings


class OllamaProvider(BaseLLMProvider):
    """Ollama LLM 프로바이더"""
    
    def __init__(self, model_name: str = None, **kwargs):
        super().__init__(
            model_name=model_name or settings.DEFAULT_LLM_MODEL,
            **kwargs
        )
    
    def get_chat_model(self, **kwargs) -> BaseChatModel:
        """Ollama 모델 인스턴스 반환"""
        model_kwargs = {
            "model": self.model_name,
            "temperature": kwargs.get("temperature", settings.TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS),
            **self.kwargs
        }
        
        return ChatOllama(**model_kwargs)
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """채팅 완성 요청"""
        model = self.get_chat_model(**kwargs)
        
        # Langchain 메시지 형식으로 변환
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                from langchain_core.messages import HumanMessage
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                from langchain_core.messages import AIMessage
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                from langchain_core.messages import SystemMessage
                langchain_messages.append(SystemMessage(content=msg["content"]))
        
        response = await model.ainvoke(langchain_messages)
        return response.content
    
    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 채팅 완성"""
        model = self.get_chat_model(**kwargs)
        
        # Langchain 메시지 형식으로 변환
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                from langchain_core.messages import HumanMessage
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                from langchain_core.messages import AIMessage
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                from langchain_core.messages import SystemMessage
                langchain_messages.append(SystemMessage(content=msg["content"]))
        
        async for chunk in model.astream(langchain_messages):
            yield chunk.content
    
    @property
    def provider_name(self) -> str:
        return "ollama"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "mistral-small3.1:latest"
        ]
