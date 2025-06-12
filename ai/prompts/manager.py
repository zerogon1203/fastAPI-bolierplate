"""프롬프트 관리자 클래스"""

from typing import Dict, Optional
from pathlib import Path
import json
import yaml

from .templates import SYSTEM_PROMPTS, USER_PROMPTS, RAG_PROMPTS


class PromptManager:
    """프롬프트 템플릿 관리자"""
    
    def __init__(self, custom_prompts_path: Optional[str] = None):
        self.system_prompts = SYSTEM_PROMPTS.copy()
        self.user_prompts = USER_PROMPTS.copy()
        self.rag_prompts = RAG_PROMPTS.copy()
        
        # 커스텀 프롬프트 로드
        if custom_prompts_path:
            self.load_custom_prompts(custom_prompts_path)
    
    def get_system_prompt(self, key: str, default: str = None) -> str:
        """시스템 프롬프트 반환"""
        return self.system_prompts.get(key, default or self.system_prompts["default_chat"])
    
    def get_user_prompt(self, key: str, **kwargs) -> str:
        """사용자 프롬프트 반환 (변수 포맷팅 포함)"""
        template = self.user_prompts.get(key)
        if not template:
            raise ValueError(f"사용자 프롬프트 '{key}'를 찾을 수 없습니다.")
        
        return template.format(**kwargs)
    
    def get_rag_prompt(self, key: str, **kwargs) -> str:
        """RAG 프롬프트 반환 (변수 포맷팅 포함)"""
        template = self.rag_prompts.get(key)
        if not template:
            raise ValueError(f"RAG 프롬프트 '{key}'를 찾을 수 없습니다.")
        
        return template.format(**kwargs)
    
    def add_system_prompt(self, key: str, prompt: str):
        """시스템 프롬프트 추가"""
        self.system_prompts[key] = prompt
    
    def add_user_prompt(self, key: str, prompt: str):
        """사용자 프롬프트 추가"""
        self.user_prompts[key] = prompt
    
    def add_rag_prompt(self, key: str, prompt: str):
        """RAG 프롬프트 추가"""
        self.rag_prompts[key] = prompt
    
    def load_custom_prompts(self, file_path: str):
        """커스텀 프롬프트 파일 로드"""
        path = Path(file_path)
        if not path.exists():
            return
        
        try:
            if path.suffix.lower() == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif path.suffix.lower() in ['.yml', '.yaml']:
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {path.suffix}")
            
            # 프롬프트 병합
            if 'system_prompts' in data:
                self.system_prompts.update(data['system_prompts'])
            if 'user_prompts' in data:
                self.user_prompts.update(data['user_prompts'])
            if 'rag_prompts' in data:
                self.rag_prompts.update(data['rag_prompts'])
        
        except Exception as e:
            print(f"커스텀 프롬프트 로드 실패: {e}")
    
    def save_prompts(self, file_path: str):
        """현재 프롬프트들을 파일로 저장"""
        path = Path(file_path)
        
        data = {
            'system_prompts': self.system_prompts,
            'user_prompts': self.user_prompts,
            'rag_prompts': self.rag_prompts
        }
        
        try:
            if path.suffix.lower() == '.json':
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif path.suffix.lower() in ['.yml', '.yaml']:
                with open(path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {path.suffix}")
        
        except Exception as e:
            print(f"프롬프트 저장 실패: {e}")
    
    def list_prompts(self) -> Dict[str, list]:
        """사용 가능한 프롬프트 목록 반환"""
        return {
            'system_prompts': list(self.system_prompts.keys()),
            'user_prompts': list(self.user_prompts.keys()),
            'rag_prompts': list(self.rag_prompts.keys())
        }
    
    def search_prompts(self, keyword: str) -> Dict[str, list]:
        """키워드로 프롬프트 검색"""
        results = {
            'system_prompts': [],
            'user_prompts': [],
            'rag_prompts': []
        }
        
        keyword_lower = keyword.lower()
        
        # 시스템 프롬프트 검색
        for key, prompt in self.system_prompts.items():
            if keyword_lower in key.lower() or keyword_lower in prompt.lower():
                results['system_prompts'].append(key)
        
        # 사용자 프롬프트 검색
        for key, prompt in self.user_prompts.items():
            if keyword_lower in key.lower() or keyword_lower in prompt.lower():
                results['user_prompts'].append(key)
        
        # RAG 프롬프트 검색
        for key, prompt in self.rag_prompts.items():
            if keyword_lower in key.lower() or keyword_lower in prompt.lower():
                results['rag_prompts'].append(key)
        
        return results 