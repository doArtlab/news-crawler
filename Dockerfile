# ----- Stage 1: Build -----
    FROM python:3.13-slim AS builder

    # Poetry 설치
    ENV PYTHONUNBUFFERED=1 POETRY_VERSION=2.1.3 POETRY_VIRTUALENVS_CREATE=false
    RUN pip install "poetry==$POETRY_VERSION"
    
    # 작업 디렉터리 생성
    WORKDIR /app
    
    # pyproject.toml, poetry.lock 복사
    COPY pyproject.toml poetry.lock README.md ./
    
    # 프로젝트 의존성 설치 (시스템-wide가 아닌 가상 env에)
    RUN poetry config virtualenvs.create false && poetry lock \
     && poetry install --no-root --only main

    # 앱 코드 복사
    COPY . .
    
    # ----- Stage 2: Runtime -----
    FROM python:3.13-slim
    
    WORKDIR /app
    
    # 필요한 시스템 패키지 (옵션)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev gcc \
     && rm -rf /var/lib/apt/lists/*   
    
    # builder 이미지에서 패키지 복사
    COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
    COPY --from=builder /usr/local/bin /usr/local/bin
    COPY --from=builder /app /app
    
    # 실행 명령
    CMD ["python", "src/main.py"]