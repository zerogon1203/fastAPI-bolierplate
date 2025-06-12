"""LLM 프로바이더 기본 클래스"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncIterator
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings


class BaseLLMProvider(ABC):
    """LLM 프로바이더 기본 추상 클래스"""
    
    def __init__(self, api_key: str, model_name: str = None, **kwargs):
        self.api_key = api_key
        self.model_name = model_name
        self.kwargs = kwargs
        self._client = None
    
    @abstractmethod
    def get_chat_model(self, **kwargs) -> BaseChatModel:
        """채팅 모델 인스턴스 반환"""
        pass
    
    @abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """채팅 완성 요청"""
        pass
    
    @abstractmethod
    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> AsyncIterator[str]:
        """스트리밍 채팅 완성"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """프로바이더 이름"""
        pass
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """사용 가능한 모델 목록"""
        pass


class BaseEmbeddingProvider(ABC):
    """임베딩 프로바이더 기본 추상 클래스"""
    
    def __init__(self, api_key: str, model_name: str = None, **kwargs):
        self.api_key = api_key
        self.model_name = model_name
        self.kwargs = kwargs
        self._client = None
    
    @abstractmethod
    def get_embeddings(self, **kwargs) -> Embeddings:
        """임베딩 모델 인스턴스 반환"""
        pass
    
    @abstractmethod
    async def embed_text(self, text: str, **kwargs) -> List[float]:
        """텍스트 임베딩"""
        pass
    
    @abstractmethod
    async def embed_documents(self, texts: List[str], **kwargs) -> List[List[float]]:
        """문서들 임베딩"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """프로바이더 이름"""
        pass
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """사용 가능한 임베딩 모델 목록"""
        pass
    
    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """임베딩 벡터 차원"""
        pass 