# 1단계: Python 3.10 slim 기반 이미지
FROM python:3.10-slim

# 2단계: 시스템 패키지 설치 (한글 OCR 포함)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    libtesseract-dev \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3단계: 작업 디렉토리 지정
WORKDIR /app

# 4단계: 파이썬 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5단계: 앱 소스 복사
COPY ./app ./app

# 6단계: 포트 노출
EXPOSE 8000

# 7단계: 앱 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
