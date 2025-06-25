import os
import sys
from string import Template

# ──────────────────────────────
# 모델 이름 받기
model_name = os.environ.get("name")
if not model_name:
    print("❌ 모델명을 'name' 인자로 전달해야 합니다. 예: make model-create name=User")
    sys.exit(1)

# snake_case 변환
snake_name = ''.join(['_' + c.lower() if c.isupper() else c for c in model_name]).lstrip('_')
file_path = f"models/{snake_name}.py"
init_file_path = "models/__init__.py"

# ──────────────────────────────
# 중복 확인
if os.path.exists(file_path):
    print(f"❌ 이미 존재하는 모델입니다: {file_path}")
    sys.exit(1)

# ──────────────────────────────
# 모델 템플릿
template = Template('''"""
${model_name} 모델 정의
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from core.database import Base
from pydantic import BaseModel


class ${model_name}(Base):
    __tablename__ = "${table_name}"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ${model_name}Create(BaseModel):
    name: str


class ${model_name}Update(BaseModel):
    name: Optional[str] = None


class ${model_name}Response(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
''')

# ──────────────────────────────
# 모델 파일 생성
with open(file_path, "w", encoding="utf-8") as f:
    f.write(template.substitute(
        model_name=model_name,
        table_name=snake_name + "s"
    ))

print(f"✅ 모델 생성 완료: {file_path}")

# ──────────────────────────────
# __init__.py에 자동 등록
import_line = f"from .{snake_name} import {model_name}\n"

# 없으면 생성
if not os.path.exists(init_file_path):
    with open(init_file_path, "w", encoding="utf-8") as f:
        f.write(import_line)
else:
    with open(init_file_path, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        if import_line not in lines:
            f.write(import_line)
            print(f"✅ models/__init__.py에 {model_name} import 등록 완료")
        else:
            print(f"⚠️ models/__init__.py에 이미 등록되어 있음")
