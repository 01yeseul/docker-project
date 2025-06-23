# 📂 파일 내 개인정보 탐지기 (PII Detector)

TXT, PDF, DOCX, 이미지(JPG, PNG) 파일에서  
**이메일, 전화번호, 주민등록번호, 이름, 주소** 등 개인정보를 자동 탐지하고  
**마스킹된 결과/다운로드용 PDF**까지 제공하는 웹서비스입니다.

---

## 🚀 주요 기능 (Features)

- 다양한 파일 지원: `TXT`, `PDF`, `DOCX`, `JPG`, `PNG`
- 개인정보(이메일, 전화번호, 주민등록번호, 이름, 도로명 주소 등) 자동 탐지
- **마스킹 기능**: 탐지된 개인정보 자동 가림처리 (이메일, 이름, 전화번호, 주민번호, 주소)
- **마스킹 결과 PDF** 다운로드 (한글폰트 지원)
- **이미지 내 문자(OCR)** 자동 탐지/마스킹 (한글/영어)
- **웹 기반 사용법 & 쉬운 UI**

---

## 🗂️ 디렉토리 구조

```plaintext
pii-detector/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI 진입점 (라우팅, 렌더링)
│   ├── detector.py           # 개인정보 탐지 및 마스킹
│   ├── file_parser.py        # 파일/이미지에서 텍스트 추출
│   ├── report_generator.py   # 마스킹 결과 PDF 저장
│   ├── static/
│   │   └── style.css         # CSS
│   ├── templates/
│   │   ├── index.html        # 업로드 폼
│   │   └── result.html       # 결과/마스킹 화면
│   ├── uploads/              # (런타임) 업로드된 파일 저장
│   └── fonts/
│       └── Pretendard-Regular.ttf   # 한글 폰트
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md


---

## ⚡ 빠른 시작 (로컬 실행)

### 1. 환경 준비

Python 3.10+  
아래 명령으로 라이브러리 설치:

```bash
pip install -r requirements.txt

OCR(이미지 문자 인식) 기능 사용 시,

시스템에 Tesseract 및 한글 데이터가 설치되어 있어야 합니다.



### 2. 실행
bash
코드 복사
uvicorn app.main:app --reload
브라우저에서 http://localhost:8000 접속

파일 업로드 → 탐지 결과 확인 → 마스킹 PDF 다운로드

🐳 Docker로 배포
1. 빌드 & 실행
# 빌드
docker compose build

# 컨테이너 실행
docker compose up

2. 서비스 확인
http://localhost:8000

업로드 파일은 app/uploads/에 저장됩니다.

🛠️ 주요 기술스택
FastAPI + Jinja2 (백엔드 & 템플릿)

PyMuPDF (fitz): PDF 텍스트 추출

python-docx: 워드(docx) 파싱

pytesseract: 이미지 내 문자 OCR

FPDF: 마스킹 결과 PDF 생성 (한글폰트)

Pillow: 이미지 로딩

Docker: 배포 환경 표준화

📝 개인정보 탐지 예시 (Types Detected)
| 유형      | 예시                                               |
| ------   | ------------------------------------------------- |
| 이메일     | [johndoe@example.com](mailto:johndoe@example.com) |
| 전화번호    | 010-1234-5678, 02-123-4567                        |
| 주민등록번호 | 900101-1234567                                    |
| 이름       | 김민수, 박민, 홍설 등 2\~3글자 한글 이름                  |
| 도로명 주소 | 무등로 123, 상무대로 77                                |


📄 라이선스
MIT License


🛑 유의사항
OCR 인식률은 이미지 품질/폰트에 따라 달라질 수 있습니다.

개인정보(이름)는 완벽 탐지가 어렵거나, 블랙리스트에 등록된 단어/고유명사 등은 예외처리됨

한글 PDF 결과물(폰트) 누락 시, app/fonts/에 Pretendard 폰트가 필요

💡 TODO & 개선점
더 다양한 개인정보 유형 탐지(외국인번호, 기업번호 등)

사용자 정의 블랙리스트/화이트리스트 UI 지원

관리자용 업로드 이력 관리 기능

마스킹 PDF 파일 암호화/삭제 등 보안 강화


