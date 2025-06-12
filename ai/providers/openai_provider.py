"""OpenAI 프로바이더 구현"""

from typing import AsyncIterator, Dict, List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from .base import BaseLLMProvider, BaseEmbeddingProvider
from core.settings import settings


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM 프로바이더"""
    
    def __init__(self, api_key: str = None, model_name: str = None, **kwargs):
        super().__init__(
            api_key=api_key or settings.OPENAI_API_KEY,
            model_name=model_name or settings.DEFAULT_LLM_MODEL,
            **kwargs
        )
    
    def get_chat_model(self, **kwargs) -> BaseChatModel:
        """ChatOpenAI 모델 인스턴스 반환"""
        model_kwargs = {
            "api_key": self.api_key,
            "model": self.model_name,
            "temperature": kwargs.get("temperature", settings.TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS),
            **self.kwargs
        }
        
        return ChatOpenAI(**model_kwargs)
    
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
        return "openai"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI 임베딩 프로바이더"""
    
    def __init__(self, api_key: str = None, model_name: str = None, **kwargs):
        super().__init__(
            api_key=api_key or settings.OPENAI_API_KEY,
            model_name=model_name or settings.DEFAULT_EMBEDDING_MODEL,
            **kwargs
        )
    
    def get_embeddings(self, **kwargs) -> Embeddings:
        """OpenAI 임베딩 모델 반환"""
        return OpenAIEmbeddings(
            api_key=self.api_key,
            model=self.model_name,
            **self.kwargs
        )
    
    async def embed_text(self, text: str, **kwargs) -> List[float]:
        """텍스트 임베딩"""
        embeddings = self.get_embeddings(**kwargs)
        return await embeddings.aembed_query(text)
    
    async def embed_documents(self, texts: List[str], **kwargs) -> List[List[float]]:
        """문서들 임베딩"""
        embeddings = self.get_embeddings(**kwargs)
        return await embeddings.aembed_documents(texts)
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    @property
    def available_models(self) -> List[str]:
        return [
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large"
        ]
    
    @property
    def embedding_dimension(self) -> int:
        """임베딩 벡터 차원"""
        model_dimensions = {
            "text-embedding-ada-002": 1536,
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072
        }
        return model_dimensions.get(self.model_name, 1536) 