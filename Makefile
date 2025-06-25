.PHONY: help install install-dev format lint test test-cov run dev clean docker-build docker-run

# 기본 명령어
help: ## 사용 가능한 명령어들을 보여줍니다
	@echo "사용 가능한 명령어:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# 설치 및 설정
install: ## 프로덕션 의존성을 설치합니다
	pip install -r requirements.txt

install-dev: ## 개발 의존성을 포함하여 설치합니다
	pip install -e ".[dev]"

# 코드 포맷팅 및 린팅
format: ## 코드를 자동으로 포맷팅합니다 (black, isort)
	black app tests
	isort app tests

lint: ## 코드 품질을 검사합니다 (flake8, mypy)
	flake8 app tests
	mypy app

# 테스트
test: ## 모든 테스트를 실행합니다
	pytest

test-cov: ## 테스트 커버리지와 함께 실행합니다
	pytest --cov=app --cov-report=term-missing --cov-report=html

test-unit: ## 단위 테스트만 실행합니다
	pytest -m unit

test-integration: ## 통합 테스트만 실행합니다
	pytest -m integration

# 개발 서버
run: ## 프로덕션 모드로 서버를 실행합니다
	uvicorn app.main:app --host 0.0.0.0 --port 8000

dev: ## 개발 모드로 서버를 실행합니다 (hot reload)
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 데이터베이스 마이그레이션
db-upgrade: ## 데이터베이스 마이그레이션을 적용합니다
	alembic upgrade head

db-downgrade: ## 데이터베이스 마이그레이션을 롤백합니다
	alembic downgrade -1

db-revision: ## 새로운 마이그레이션을 생성합니다
	alembic revision --autogenerate -m "$(msg)"

db-init: ## 데이터베이스를 초기화합니다
	alembic init alembic

# 정리
clean: ## 임시 파일들을 정리합니다
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/

# Docker 관련
docker-build: ## Docker 이미지를 빌드합니다
	docker build -t fastapi-boilerplate .

docker-run: ## Docker 컨테이너를 실행합니다
	docker run -p 8000:8000 --env-file .env fastapi-boilerplate

docker-compose-up: ## Docker Compose로 전체 스택을 실행합니다
	docker-compose up -d

docker-compose-down: ## Docker Compose 스택을 종료합니다
	docker-compose down

# 전체 품질 검사
check: format lint test ## 포맷팅, 린팅, 테스트를 모두 실행합니다

# 개발 환경 초기 설정
setup: install-dev ## 개발 환경을 초기 설정합니다
	cp env.example .env
	@echo "env.example을 .env로 복사했습니다. 환경 변수를 수정해주세요."

# 보안 검사
security: ## 보안 취약점을 검사합니다 (bandit, safety)
	bandit -r app/
	safety check

# AI 관련 명령어
ai-test: ## AI 기능들을 테스트합니다
	pytest tests/test_ai/ -v

langchain-serve: ## Langchain 서버를 실행합니다
	langchain serve --port=8001

mcp-test: ## MCP 서버 연결을 테스트합니다
	python -m app.ai.mcp.test_server

ai-setup: ## AI 관련 초기 설정을 진행합니다
	@echo "AI 서비스 API 키를 .env 파일에 설정해주세요:"
	@echo "- OPENAI_API_KEY"
	@echo "- ANTHROPIC_API_KEY"
	@echo "- LANGCHAIN_API_KEY"

# 문서 생성
docs: ## API 문서를 생성합니다
	@echo "FastAPI 자동 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다." 

# Secret Key 생성
gen-secret-key: ## Secret Key를 생성합니다
	python -c "import secrets; print(secrets.token_urlsafe(32))"