# AI 통합 가이드 (Langchain + MCP)

## 개요

이 보일러플레이트는 AI 시대를 대비하여 Langchain과 MCP(Model Context Protocol)를 기본적으로 지원합니다.

## 기능

### 🔗 Langchain 통합
- **다중 LLM 프로바이더 지원**: OpenAI, Anthropic, Google 등
- **LangServe**: FastAPI와 Langchain 체인 통합
- **RAG (Retrieval-Augmented Generation)**: 문서 기반 QA 시스템
- **AI 에이전트**: 자동화된 작업 수행
- **벡터 검색**: 의미 기반 문서 검색

### 🤖 MCP (Model Context Protocol) 지원
- **표준 프로토콜**: AI 애플리케이션 간 상호운용성
- **다양한 서버**: 파일시스템, GitHub, Slack 등 연동
- **커스텀 서버**: 비즈니스 로직을 MCP 서버로 노출
- **안전한 통신**: 클라이언트-서버 간 안전한 데이터 교환

## 설정 방법

### 1. API 키 설정

`.env` 파일에 필요한 API 키들을 설정하세요:

```bash
# 필수 LLM API 키 (하나 이상)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Langchain 모니터링 (선택사항)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=fastapi-boilerplate

# 벡터 데이터베이스 (선택사항)
PINECONE_API_KEY=your-pinecone-api-key
WEAVIATE_URL=http://localhost:8080
```

### 2. MCP 서버 설정

`config/mcp_servers.json` 파일에서 사용할 MCP 서버들을 설정하세요.

### 3. AI 초기 설정

```bash
make ai-setup
```

## 사용 예시

### Langchain 체인 예시

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.ai.providers.openai_provider import get_openai_llm

# 프롬프트 템플릿 정의
template = """
다음 질문에 한국어로 답변해주세요:
질문: {question}
답변:
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

# LLM 체인 생성
llm = get_openai_llm()
chain = LLMChain(llm=llm, prompt=prompt)

# 실행
result = chain.run(question="FastAPI의 장점은 무엇인가요?")
```

### MCP 서버 구현 예시

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context

# MCP 서버 생성
mcp = FastMCP("database-tools")

@mcp.tool()
async def get_user_count(ctx: Context) -> str:
    """사용자 수를 조회합니다"""
    # 실제 데이터베이스 쿼리 로직
    count = await get_user_count_from_db()
    return f"전체 사용자 수: {count}명"

@mcp.resource("users://{user_id}")
def get_user_profile(user_id: str) -> str:
    """사용자 프로필을 조회합니다"""
    # 사용자 정보 조회 로직
    profile = get_user_profile_from_db(user_id)
    return f"사용자 정보: {profile}"
```

### RAG 시스템 예시

```python
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from app.ai.providers.openai_provider import get_openai_llm

# 벡터 저장소 설정
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(
    documents, 
    embeddings, 
    index_name="knowledge-base"
)

# RAG 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=get_openai_llm(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 질문 답변
answer = qa_chain.run("회사 정책에 대해 알려주세요")
```

## 디렉토리 구조

```
app/ai/
├── chains/              # Langchain 체인들
│   ├── __init__.py
│   ├── qa_chain.py     # Q&A 체인
│   ├── summary_chain.py # 요약 체인
│   └── analysis_chain.py # 분석 체인
├── agents/              # AI 에이전트들
│   ├── __init__.py
│   ├── data_agent.py   # 데이터 분석 에이전트
│   └── support_agent.py # 고객 지원 에이전트
├── tools/               # AI 도구들
│   ├── __init__.py
│   ├── database_tools.py # 데이터베이스 도구
│   └── api_tools.py    # API 호출 도구
├── prompts/             # 프롬프트 템플릿
│   ├── __init__.py
│   ├── qa_prompts.py   # Q&A 프롬프트
│   └── analysis_prompts.py # 분석 프롬프트
├── embeddings/          # 임베딩 관련
│   ├── __init__.py
│   └── vector_store.py # 벡터 저장소 관리
├── memory/              # 대화 메모리
│   ├── __init__.py
│   └── chat_memory.py  # 채팅 메모리 관리
├── mcp/                 # MCP 서버/클라이언트
│   ├── servers/         # MCP 서버 구현
│   │   ├── __init__.py
│   │   ├── database_server.py # 데이터베이스 MCP 서버
│   │   └── custom_server.py   # 커스텀 MCP 서버
│   ├── clients/         # MCP 클라이언트
│   │   ├── __init__.py
│   │   └── mcp_client.py # MCP 클라이언트 래퍼
│   └── tools/           # MCP 도구들
│       ├── __init__.py
│       └── mcp_tools.py # MCP 도구 정의
└── providers/           # LLM 프로바이더 설정
    ├── __init__.py
    ├── openai_provider.py    # OpenAI 설정
    ├── anthropic_provider.py # Anthropic 설정
    └── base_provider.py      # 기본 프로바이더 인터페이스
```

## API 엔드포인트 예시

### AI 채팅 API

```python
@router.post("/ai/chat")
async def chat_with_ai(request: ChatRequest):
    """AI와 채팅합니다"""
    chain = get_chat_chain()
    response = await chain.arun(
        message=request.message,
        history=request.history
    )
    return {"response": response}
```

### 문서 분석 API

```python
@router.post("/ai/analyze-document")
async def analyze_document(file: UploadFile):
    """문서를 분석합니다"""
    # 파일 처리
    text = extract_text_from_file(file)
    
    # AI 분석
    analysis_chain = get_analysis_chain()
    result = await analysis_chain.arun(text=text)
    
    return {"analysis": result}
```

### RAG 검색 API

```python
@router.post("/ai/search")
async def search_knowledge(query: SearchQuery):
    """지식 기반에서 검색합니다"""
    qa_chain = get_qa_chain()
    answer = await qa_chain.arun(question=query.question)
    return {"answer": answer}
```

## 모니터링 및 관찰성

### LangSmith 통합
- Langchain 실행 추적
- 성능 모니터링
- 디버깅 지원

### 메트릭 수집
- 토큰 사용량 추적
- 응답 시간 측정
- 에러율 모니터링

## 보안 고려사항

### 입력 검증
- 프롬프트 주입 방지
- 입력 데이터 sanitization
- Rate limiting 적용

### API 키 보안
- 환경 변수로 관리
- 키 로테이션 정책
- 최소 권한 원칙

## 확장 가능성

### 새로운 LLM 프로바이더 추가
1. `app/ai/providers/` 에 새 프로바이더 추가
2. 기본 프로바이더 인터페이스 구현
3. 환경 설정 추가

### 커스텀 MCP 서버 개발
1. `app/ai/mcp/servers/` 에 새 서버 추가
2. MCP 프로토콜 구현
3. 설정 파일에 서버 등록

### AI 기능 확장
1. 새로운 체인이나 에이전트 개발
2. 커스텀 도구 추가
3. 프롬프트 템플릿 확장

## 테스트

```bash
# AI 기능 테스트
make ai-test

# MCP 서버 테스트
make mcp-test

# Langchain 서버 실행
make langchain-serve
```

## 문제 해결

### 자주 발생하는 문제들

1. **API 키 오류**: `.env` 파일의 API 키 확인
2. **MCP 연결 실패**: MCP 서버 설정 및 네트워크 확인
3. **메모리 부족**: 큰 문서 처리 시 청크 크기 조정
4. **토큰 한도 초과**: 프롬프트 크기 최적화

### 로그 확인

```bash
# AI 관련 로그 확인
tail -f logs/ai.log

# MCP 서버 로그 확인
tail -f logs/mcp.log
```

이 가이드를 참고하여 AI 기능을 효과적으로 활용하세요! 🚀 