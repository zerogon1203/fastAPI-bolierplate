"""Anthropic 프로바이더 구현"""

from typing import AsyncIterator, Dict, List
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from .base import BaseLLMProvider
from core.settings import settings


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude 프로바이더"""
    
    def __init__(self, api_key: str = None, model_name: str = None, **kwargs):
        super().__init__(
            api_key=api_key or settings.ANTHROPIC_API_KEY,
            model_name=model_name or "claude-3-haiku-20240307",
            **kwargs
        )
    
    def get_chat_model(self, **kwargs) -> BaseChatModel:
        """ChatAnthropic 모델 인스턴스 반환"""
        model_kwargs = {
            "anthropic_api_key": self.api_key,
            "model": self.model_name,
            "temperature": kwargs.get("temperature", settings.TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS),
            **self.kwargs
        }
        
        return ChatAnthropic(**model_kwargs)
    
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
        return "anthropic"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022",
            "claude-2.1",
            "claude-2.0"
        ] 