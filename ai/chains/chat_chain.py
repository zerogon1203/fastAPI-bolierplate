"""기본 채팅 체인 구현"""

from typing import Dict, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from ai.providers import get_llm_provider
from ai.prompts import PromptManager


class ChatChain:
    """기본 채팅 체인 클래스"""
    
    def __init__(
        self,
        provider_name: str = "openai",
        model_name: str = None,
        system_message: str = None,
        **kwargs
    ):
        self.provider = get_llm_provider(
            provider_name=provider_name,
            model_name=model_name,
            **kwargs
        )
        self.llm = self.provider.get_chat_model()
        self.prompt_manager = PromptManager()
        
        # 시스템 메시지 설정
        if system_message is None:
            system_message = self.prompt_manager.get_system_prompt("default_chat")
        
        # 프롬프트 템플릿 생성
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 체인 구성
        self.chain = self.prompt | self.llm
    
    async def ainvoke(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """비동기 채팅 완성"""
        # 메시지 형식 변환
        langchain_messages = self._convert_messages(messages)
        
        # 체인 실행
        response = await self.chain.ainvoke({
            "messages": langchain_messages
        })
        
        return response.content
    
    async def astream(self, messages: List[Dict[str, str]], **kwargs):
        """비동기 스트리밍 채팅"""
        langchain_messages = self._convert_messages(messages)
        
        async for chunk in self.chain.astream({
            "messages": langchain_messages
        }):
            yield chunk.content
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[BaseMessage]:
        """메시지 형식 변환"""
        langchain_messages = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            elif role == "system":
                langchain_messages.append(SystemMessage(content=content))
        
        return langchain_messages


def get_chat_chain(
    provider_name: str = "openai",
    model_name: str = None,
    system_message: str = None,
    **kwargs
) -> ChatChain:
    """채팅 체인 인스턴스 생성
    
    Args:
        provider_name: LLM 프로바이더 이름
        model_name: 모델 이름
        system_message: 시스템 메시지
        **kwargs: 추가 설정
    
    Returns:
        ChatChain: 채팅 체인 인스턴스
    """
    return ChatChain(
        provider_name=provider_name,
        model_name=model_name,
        system_message=system_message,
        **kwargs
    ) 