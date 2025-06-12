# FastAPI AI 보일러플레이트

🚀 AI 시대를 위한 프로덕션 레디 FastAPI 보일러플레이트

## 📋 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 설정](#설치-및-설정)
- [사용법](#사용법)
- [API 문서](#api-문서)
- [디렉토리 구조](#디렉토리-구조)
- [개발 가이드](#개발-가이드)
- [배포](#배포)
- [환경 변수](#환경-변수)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 개요

이 프로젝트는 AI/LLM 통합에 특화된 현대적이고 확장 가능한 FastAPI 보일러플레이트입니다. 엔터프라이즈급 애플리케이션 개발을 위한 모든 필수 기능과 AI 시대에 맞는 최신 기술들을 포함하고 있습니다.

## 주요 기능

### 🔐 인증 및 보안
- JWT 토큰 기반 인증
- 역할 기반 접근 제어 (RBAC)
- 비밀번호 해싱 (bcrypt)
- CORS 및 보안 미들웨어
- 요청 속도 제한

### 🤖 AI/LLM 통합
- **완전한 AI 모듈 구조** - providers, chains, prompts, tools 등 체계적 구성
- **다중 AI 프로바이더** 지원 (OpenAI, Anthropic, Google)
- **Langchain 체인** - 채팅, RAG, 문서분석 체인 기본 제공
- **프롬프트 관리 시스템** - 템플릿 기반 프롬프트 관리
- **MCP (Model Context Protocol)** 서버 통합
- **RAG (Retrieval-Augmented Generation)** 검색
- **문서 분석** 및 처리
- **벡터 데이터베이스** 연동 (Chroma, Pinecone, Weaviate)
- **AI 도구 호출** 기능

### 🗄️ 데이터베이스
- **비동기 SQLAlchemy** ORM
- **다중 데이터베이스 지원** (PostgreSQL, MySQL, SQLite)
- **모듈식 설정** - URL 대신 개별 환경변수
- 커넥션 풀링 및 최적화
- 데이터베이스 마이그레이션 (Alembic)

### 💾 파일 스토리지
- **다중 스토리지 백엔드** (로컬, AWS S3)
- **자동 파일명 처리** - 안전한 파일명 생성
- **파일 크기 제한** 및 검증
- **MinIO 지원** - S3 호환 스토리지

### 📊 모니터링 및 로깅
- **Loguru** 기반 구조화 로깅
- 로그 레벨별 파일 분리
- AI 전용 로그 추적
- 헬스체크 엔드포인트
- Kubernetes 호환 프로브

### 🛠️ 개발자 경험
- **자동 API 문서화** (OpenAPI/Swagger)
- **타입 힌트** 완전 지원
- **환경별 설정** 관리
- **Docker** 컨테이너화
- **개발 도구** 통합 (Black, isort, flake8, mypy)

## 기술 스택

### Backend
- **FastAPI** - 고성능 웹 프레임워크
- **Python 3.12+** - 최신 Python 기능 활용
- **SQLAlchemy** - 비동기 ORM
- **다중 데이터베이스** - PostgreSQL, MySQL, SQLite 지원
- **Redis** - 캐싱 및 세션 스토어
- **모듈식 설정** - 환경변수 기반 유연한 구성

### AI/ML
- **Langchain** - LLM 애플리케이션 프레임워크
- **Langsmith** - LLM 추적 및 모니터링
- **MCP** - Model Context Protocol
- **OpenAI/Anthropic/Google** - AI 프로바이더
- **벡터 데이터베이스** - 임베딩 스토리지

### Storage & Infrastructure
- **다중 파일 스토리지** - 로컬, AWS S3, MinIO 지원
- **환경별 설정** - 개발/테스트/프로덕션 분리
- **Docker** - 컨테이너화
- **Docker Compose** - 로컬 개발 환경
- **Kubernetes** - 프로덕션 배포
- **GitHub Actions** - CI/CD

## 설치 및 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/fastapi-ai-boilerplate.git
cd fastapi-ai-boilerplate
```

### 2. Python 환경 설정
```bash
# Python 3.12+ 필요
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 실제 값들을 입력하세요
```

### 5. 데이터베이스 설정

#### PostgreSQL 사용 (기본값)
```bash
# PostgreSQL 시작 (Docker 사용)
make db-start

# 데이터베이스 마이그레이션
make db-migrate
```

#### SQLite 사용 (간편 개발)
```bash
# .env 파일에서 DB_TYPE을 sqlite로 변경
echo "DB_TYPE=sqlite" >> .env
echo "SQLITE_DATABASE_PATH=./data/app.db" >> .env

# 데이터베이스 초기화
mkdir -p data
make db-migrate
```

#### MySQL 사용
```bash
# .env 파일에서 MySQL 설정
echo "DB_TYPE=mysql" >> .env
echo "DB_PORT=3306" >> .env
# 기타 MySQL 설정...

# MySQL 시작 후 마이그레이션
make db-migrate
```

### 6. 애플리케이션 실행
```bash
# 개발 모드
make dev

# 또는 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 사용법

### Makefile 명령어

개발 편의를 위한 주요 명령어들:

```bash
# 개발 서버 시작
make dev

# 테스트 실행
make test

# 코드 포맷팅
make format

# 코드 린팅
make lint

# 타입 체크
make type-check

# 데이터베이스 관리
make db-start      # PostgreSQL 시작
make db-stop       # PostgreSQL 중지
make db-migrate    # 마이그레이션 실행
make db-reset      # 데이터베이스 리셋

# AI 기능
make ai-test       # AI 기능 테스트
make vector-reset  # 벡터 데이터베이스 리셋

# 보안 검사
make security-check

# 전체 CI 체크
make ci
```

### API 사용 예시

#### 1. 사용자 등록 및 로그인
```bash
# 사용자 등록
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "홍길동"
  }'

# 로그인
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "securepassword"
  }'
```

#### 2. AI 채팅
```bash
# AI 채팅 (인증 토큰 필요)
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "안녕하세요! FastAPI에 대해 설명해주세요.",
    "provider": "openai",
    "model": "gpt-4"
  }'
```

#### 3. 문서 분석
```bash
# 문서 업로드 및 분석
curl -X POST "http://localhost:8000/api/v1/ai/analyze-document" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

#### 4. 파일 업로드 (로컬 스토리지)
```bash
# 파일 업로드
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@example.jpg" \
  -F "folder=images"
```

#### 5. 파일 업로드 (S3 스토리지)
```bash
# S3 설정 후 같은 API로 업로드
# FILE_STORAGE_TYPE=s3로 설정하면 자동으로 S3에 저장
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

## API 문서

애플리케이션 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 디렉토리 구조

```
fastapi-ai-boilerplate/
├── app/                          # 메인 애플리케이션
│   ├── __init__.py
│   ├── main.py                   # FastAPI 앱 진입점
│   └── api/                      # API 라우터들
│       ├── __init__.py
│       ├── deps.py               # 의존성 주입
│       └── v1/                   # API v1
│           ├── __init__.py
│           ├── api.py            # 메인 API 라우터
│           └── endpoints/        # 엔드포인트 모듈들
│               ├── __init__.py
│               ├── auth.py       # 인증 API
│               ├── users.py      # 사용자 API
│               ├── health.py     # 헬스체크 API
│               └── ai.py         # AI 관련 API
├── ai/                           # AI/LLM 통합 모듈
│   ├── __init__.py
│   ├── providers/                # LLM 프로바이더들
│   │   ├── __init__.py
│   │   ├── base.py               # 프로바이더 기본 클래스
│   │   ├── openai_provider.py    # OpenAI 구현
│   │   ├── anthropic_provider.py # Anthropic 구현
│   │   ├── google_provider.py    # Google 구현
│   │   └── factory.py            # 프로바이더 팩토리
│   ├── chains/                   # Langchain 체인들
│   │   ├── __init__.py
│   │   ├── chat_chain.py         # 기본 채팅 체인
│   │   ├── rag_chain.py          # RAG 체인
│   │   └── document_analysis_chain.py
│   ├── prompts/                  # 프롬프트 템플릿
│   │   ├── __init__.py
│   │   ├── templates.py          # 프롬프트 정의
│   │   └── manager.py            # 프롬프트 관리자
│   ├── agents/                   # AI 에이전트들
│   ├── tools/                    # AI 도구들
│   ├── embeddings/               # 임베딩 관련
│   ├── memory/                   # 대화 메모리
│   └── mcp/                      # MCP 서버/클라이언트
│       ├── servers/              # MCP 서버 구현
│       ├── clients/              # MCP 클라이언트
│       └── tools/                # MCP 도구들
├── models/                       # 데이터 모델 (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py                   # 사용자 모델
│   ├── ai_conversation.py        # AI 대화 모델
│   ├── document.py               # 문서 모델
│   └── file_upload.py            # 파일 업로드 모델
├── schemas/                      # Pydantic 스키마
│   ├── __init__.py
│   ├── auth.py                   # 인증 스키마
│   ├── ai.py                     # AI 관련 스키마
│   ├── file.py                   # 파일 스키마
│   └── common.py                 # 공통 스키마
├── services/                     # 비즈니스 로직 서비스
│   ├── __init__.py
│   ├── auth_service.py           # 인증 서비스
│   ├── ai_service.py             # AI 서비스
│   ├── file_service.py           # 파일 서비스
│   └── user_service.py           # 사용자 서비스
├── utils/                        # 유틸리티 함수들
│   ├── __init__.py
│   ├── text_processing.py        # 텍스트 처리
│   ├── file_utils.py             # 파일 유틸리티
│   ├── date_utils.py             # 날짜/시간 유틸리티
│   ├── security_utils.py         # 보안 유틸리티
│   └── ai_utils.py               # AI 유틸리티
├── core/                         # 핵심 설정 및 유틸리티
│   ├── __init__.py
│   ├── settings.py               # 애플리케이션 설정
│   ├── database.py               # 데이터베이스 설정
│   ├── storage.py                # 파일 스토리지 관리
│   ├── security.py               # 보안 유틸리티
│   └── logging.py                # 로깅 설정
├── config/                       # 외부 설정 파일들
│   └── mcp_servers.json          # MCP 서버 설정
├── docs/                         # 문서
│   ├── PROJECT_RULES.md          # 프로젝트 규칙
│   └── AI_INTEGRATION_GUIDE.md   # AI 통합 가이드
├── tests/                        # 테스트 파일들
├── logs/                         # 로그 파일들
├── data/                         # 데이터 파일들 (SQLite, 벡터DB 등)
├── uploads/                      # 로컬 업로드 파일들
├── static/                       # 정적 파일들
├── requirements.txt              # Python 의존성
├── pyproject.toml               # 프로젝트 설정
├── Makefile                     # 개발 명령어
├── .env.example                 # 환경 변수 예시
├── .gitignore                   # Git 제외 파일
├── LICENSE                      # MIT 라이센스
└── README.md                    # 이 파일
```

## 개발 가이드

### 코딩 컨벤션

이 프로젝트는 다음 코딩 스타일을 따릅니다:

- **Black** - 코드 포맷터
- **isort** - import 정렬
- **flake8** - 린터
- **mypy** - 타입 체커

코드 작성 전 반드시 다음을 실행하세요:
```bash
make format  # 코드 포맷팅
make lint    # 린팅 체크
make type-check  # 타입 체크
```

### 새로운 API 엔드포인트 추가

1. `app/api/v1/endpoints/`에 새 모듈 생성
2. 라우터 및 엔드포인트 함수 정의
3. `app/api/v1/api.py`에 라우터 추가
4. 테스트 케이스 작성

### 새로운 데이터베이스 지원 추가

1. `core/database.py`의 `build_database_url()` 함수 수정
2. 새로운 드라이버를 `requirements.txt`에 추가
3. 환경변수 및 설정 추가
4. 연결 테스트 및 문서 업데이트

### 새로운 스토리지 백엔드 추가

1. `core/storage.py`에 새로운 백엔드 클래스 생성
2. `StorageBackend` 추상 클래스 상속
3. `FileStorageManager._get_backend()` 메서드 수정
4. 필요한 의존성 및 설정 추가

### AI 기능 확장

#### 새로운 AI 프로바이더 추가
1. `ai/providers/`에 새 프로바이더 클래스 생성
2. `BaseLLMProvider` 추상 클래스 상속
3. `factory.py`에 프로바이더 등록
4. 환경변수 및 설정 추가

#### 새로운 체인 추가
1. `ai/chains/`에 새 체인 클래스 생성
2. Langchain 패턴 따라 구현
3. `__init__.py`에 export 추가

#### 프롬프트 템플릿 추가
1. `ai/prompts/templates.py`에 새 템플릿 추가
2. `PromptManager`를 통해 관리
3. JSON/YAML 파일로 외부 관리 가능

더 자세한 내용은 `docs/AI_INTEGRATION_GUIDE.md`를 참조하세요.

## 배포

### Docker를 사용한 배포

```bash
# Docker 이미지 빌드
docker build -t fastapi-ai-app .

# 컨테이너 실행
docker run -p 8000:8000 fastapi-ai-app
```

### Docker Compose를 사용한 전체 스택 배포

```bash
# 전체 스택 시작 (앱 + DB + Redis)
docker-compose up -d

# 로그 확인
docker-compose logs -f app
```

### Kubernetes 배포

Kubernetes 매니페스트 파일들은 `k8s/` 디렉토리에 있습니다:

```bash
kubectl apply -f k8s/
```

## 환경 변수

주요 환경 변수들:

```bash
# 기본 설정
ENVIRONMENT=development
SECRET_KEY=your-secret-key
DEBUG=true

# 데이터베이스 (모듈식 설정)
DB_TYPE=postgresql  # postgresql, mysql, sqlite
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=username
DB_PASSWORD=password

# 파일 스토리지
FILE_STORAGE_TYPE=local  # local, s3
LOCAL_UPLOAD_DIR=./uploads

# S3 설정 (FILE_STORAGE_TYPE=s3인 경우)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=your-bucket

# AI 프로바이더
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key

# 벡터 데이터베이스
CHROMADB_PERSIST_DIRECTORY=./data/chromadb
PINECONE_API_KEY=your-pinecone-key

# 모니터링
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_PROJECT=your-project
```

전체 환경 변수 목록은 `.env.example` 파일을 참조하세요.

## 설정 가이드

### 데이터베이스 설정

#### PostgreSQL 사용
```bash
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=username
DB_PASSWORD=password
```

#### MySQL 사용
```bash
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fastapi_db
DB_USER=username
DB_PASSWORD=password
```

#### SQLite 사용 (개발용)
```bash
DB_TYPE=sqlite
SQLITE_DATABASE_PATH=./data/app.db
```

### 파일 스토리지 설정

#### 로컬 스토리지 사용
```bash
FILE_STORAGE_TYPE=local
LOCAL_UPLOAD_DIR=./uploads
LOCAL_STATIC_DIR=./static
```

#### AWS S3 사용
```bash
FILE_STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-northeast-2
S3_BUCKET_NAME=your-bucket-name
S3_PUBLIC_READ=true
```

#### MinIO 사용 (S3 호환)
```bash
FILE_STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=minio-access-key
AWS_SECRET_ACCESS_KEY=minio-secret-key
S3_BUCKET_NAME=your-bucket
S3_ENDPOINT_URL=http://localhost:9000
```

## 성능 최적화

### 데이터베이스 최적화
- 커넥션 풀링 활용
- 적절한 인덱스 설정
- 쿼리 최적화
- 데이터베이스별 최적화 설정

### 파일 스토리지 최적화
- S3 멀티파트 업로드
- CDN 연동 (CloudFront)
- 파일 압축 및 최적화

### AI 서비스 최적화
- 응답 캐싱
- 배치 처리
- 비동기 처리

### 모니터링
- 애플리케이션 메트릭 수집
- AI 응답 시간 추적
- 에러 로그 모니터링

## 보안 고려사항

### 데이터베이스 보안
- 환경 변수로 DB 인증 정보 관리
- 프로덕션에서 강력한 패스워드 사용
- DB 연결 암호화 (SSL/TLS)
- 정기적인 백업 및 복구 계획

### 파일 스토리지 보안
- S3 버킷 권한 최소화
- 업로드 파일 검증 및 스캔
- 안전한 파일명 생성 (경로 탐색 방지)
- 파일 크기 및 타입 제한

### 애플리케이션 보안
- 환경 변수로 민감한 정보 관리
- JWT 토큰 보안 및 만료 관리
- API 요청 속도 제한
- 입력 데이터 검증 및 sanitization
- AI 프롬프트 인젝션 방지
- CORS 설정 최적화

## 기여하기

1. 이 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

### 기여 가이드라인

- 코드 스타일 가이드를 따라주세요
- 테스트를 작성해주세요
- 문서를 업데이트해주세요
- 커밋 메시지는 명확하게 작성해주세요

## 문제 신고

버그나 기능 요청이 있으시면 [GitHub Issues](https://github.com/zerogon1203/fastapi-ai-boilerplate/issues)를 사용해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 특별 기능

### 🔄 자동 스토리지 전환
환경변수 하나만 바꾸면 로컬 스토리지에서 S3로 자동 전환:
```bash
# 개발 환경 (로컬)
FILE_STORAGE_TYPE=local

# 프로덕션 환경 (S3)
FILE_STORAGE_TYPE=s3
```

### 🔄 데이터베이스 유연성
개발 단계에 따라 데이터베이스를 쉽게 변경:
```bash
# 초기 개발 (SQLite)
DB_TYPE=sqlite

# 팀 개발 (PostgreSQL)
DB_TYPE=postgresql

# 프로덕션 (MySQL 클러스터)
DB_TYPE=mysql
```

### 🧪 테스트 친화적
테스트 환경은 자동으로 SQLite를 사용하여 빠른 테스트 실행

### 🏗️ 완전한 AI 아키텍처
```python
# AI 프로바이더 사용 예시
from ai.providers import get_llm_provider

provider = get_llm_provider("openai", model_name="gpt-4")
response = await provider.chat_completion([
    {"role": "user", "content": "안녕하세요!"}
])

# 프롬프트 관리자 사용
from ai.prompts import PromptManager

prompt_manager = PromptManager()
system_prompt = prompt_manager.get_system_prompt("code_assistant")
user_prompt = prompt_manager.get_user_prompt("code_review", 
                                             language="python", 
                                             code="def hello(): print('world')")
```

### 📁 모듈식 설계
```python
# 서비스 레이어 사용
from services import AIService, FileService

ai_service = AIService()
file_service = FileService()

# 스키마 기반 데이터 검증
from schemas.ai import ChatRequest

request = ChatRequest(
    message="FastAPI에 대해 설명해주세요",
    provider="openai",
    temperature=0.7
)
```

## 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들에 기반하여 만들어졌습니다:

- [FastAPI](https://fastapi.tiangolo.com/) - 현대적인 웹 프레임워크
- [Langchain](https://python.langchain.com/) - LLM 애플리케이션 개발
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 데이터 검증
- [boto3](https://boto3.amazonaws.com/) - AWS SDK

## 지원

도움이 필요하시면 다음을 참조하세요:

- [문서](docs/)
- [FAQ](docs/FAQ.md)
- [GitHub Discussions](https://github.com/zerogon1203/fastapi-ai-boilerplate/discussions)
- [이메일](mailto:zerogon@amuz.co.kr)

---

**AI 시대의 웹 개발을 위한 최고의 시작점** 🚀 