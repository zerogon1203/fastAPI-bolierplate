#!/bin/bash

# FastAPI AI 보일러플레이트 패키지 설치 스크립트

echo "🚀 FastAPI AI 보일러플레이트 패키지 설치 시작..."
echo ""
echo "📋 설치 방식을 선택해주세요:"
echo "1) requirements.txt (전체 패키지 - 모든 AI 프로바이더, 벡터DB, 파일 스토리지 포함)"
echo "2) requirements-minimal.txt (핵심 패키지만 - 기본 FastAPI + OpenAI만)"
echo "3) 단계별 맞춤 설치 (선택적으로 필요한 패키지만)"
echo ""
read -p "선택하세요 (1/2/3): " install_choice

case $install_choice in
  1)
    echo "📦 전체 패키지 설치 (requirements.txt)..."
    pip install -r requirements.txt
    echo "✅ 전체 패키지 설치 완료!"
    ;;
  2)
    echo "📦 최소 패키지 설치 (requirements-minimal.txt)..."
    pip install -r requirements-minimal.txt
    echo "✅ 최소 패키지 설치 완료!"
    ;;
  3)
    echo "📦 단계별 맞춤 설치를 시작합니다..."
    
    # 1단계: 핵심 웹 프레임워크
    echo "📦 1단계: 핵심 웹 프레임워크 설치..."
    pip install fastapi[standard]==0.115.5 uvicorn[standard]==0.32.1

# 2단계: 데이터베이스
echo "📦 2단계: 데이터베이스 패키지 설치..."
pip install sqlalchemy==2.0.36 alembic==1.14.0 asyncpg==0.30.0 aiosqlite==0.19.0

# 3단계: 인증 및 보안
echo "📦 3단계: 인증 및 보안 패키지 설치..."
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.17

# 4단계: 설정 및 유틸리티
echo "📦 4단계: 설정 및 유틸리티 패키지 설치..."
pip install python-dotenv==1.0.1 pydantic==2.10.3 pydantic-settings==2.6.1 pyyaml==6.0.2

# 5단계: 캐싱 및 HTTP
echo "📦 5단계: 캐싱 및 HTTP 클라이언트 설치..."
pip install redis==5.2.1 httpx==0.28.1

# 6단계: 로깅
echo "📦 6단계: 로깅 패키지 설치..."
pip install loguru==0.7.3

# 7단계: 기본 AI 패키지
echo "📦 7단계: 기본 AI 패키지 설치..."
    pip install langchain==0.3.18 langchain-core==0.3.63
pip install langchain-openai==0.2.14

# 8단계: 추가 AI 프로바이더 (선택사항)
echo "📦 8단계: 추가 AI 프로바이더 설치 (선택사항)..."
read -p "Anthropic Claude 지원을 설치하시겠습니까? (y/n): " install_anthropic
if [[ $install_anthropic == "y" || $install_anthropic == "Y" ]]; then
    pip install langchain-anthropic==0.3.15
fi

read -p "Google Gemini 지원을 설치하시겠습니까? (y/n): " install_google
if [[ $install_google == "y" || $install_google == "Y" ]]; then
    pip install langchain-google-genai==2.0.8
fi

read -p "Ollama 지원을 설치하시겠습니까? (y/n): " install_ollama
if [[ $install_ollama == "y" || $install_ollama == "Y" ]]; then
    pip install langchain-ollama==0.2.14
fi

# 9단계: 파일 처리
echo "📦 9단계: 파일 처리 패키지 설치..."
pip install python-magic==0.4.27

read -p "AWS S3 지원을 설치하시겠습니까? (y/n): " install_s3
if [[ $install_s3 == "y" || $install_s3 == "Y" ]]; then
    pip install boto3==1.35.83
fi

# 10단계: 개발 도구
echo "📦 10단계: 개발 도구 설치..."
pip install pytest==8.3.4 pytest-asyncio==0.24.0
pip install black==24.10.0 isort==5.13.2

# 11단계: 벡터 데이터베이스 (선택사항)
read -p "벡터 데이터베이스(ChromaDB) 지원을 설치하시겠습니까? (y/n): " install_vector
if [[ $install_vector == "y" || $install_vector == "Y" ]]; then
    pip install chromadb==0.4.24
fi

    echo "✅ 단계별 패키지 설치 완료!"
    ;;
  *)
    echo "❌ 잘못된 선택입니다. 1, 2, 또는 3을 선택해주세요."
    exit 1
    ;;
esac

echo ""
echo "🔧 다음 단계:"
echo "1. cp env.example .env"
echo "2. .env 파일 편집"
echo "3. mkdir -p data logs uploads static"
echo "4. python -m uvicorn app.main:app --reload" 