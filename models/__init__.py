"""데이터 모델 정의"""

from .user import User, UserCreate, UserUpdate
# from .ai_conversation import AIConversation, AIMessage  # TODO: 구현 필요
# from .document import Document, DocumentChunk  # TODO: 구현 필요
# from .file_upload import FileUpload  # TODO: 구현 필요

__all__ = [
    "User",
    "UserCreate", 
    "UserUpdate",
    # "AIConversation",  # TODO: 구현 후 주석 해제
    # "AIMessage",
    # "Document",
    # "DocumentChunk", 
    # "FileUpload",
] 