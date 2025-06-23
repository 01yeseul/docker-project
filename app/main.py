from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os
from .file_parser import extract_text_from_file
from .detector import detect_personal_info, mask_personal_info
from .report_generator import save_masked_pdf


# FastAPI 앱 생성
app = FastAPI()

# 정적 파일 & 템플릿 설정
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 업로드 폴더
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 📍 메인 화면 - 업로드 폼
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 📍 파일 업로드 처리
@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    # 업로드된 파일 저장
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 텍스트 추출 → 탐지 → 마스킹
    extracted_text = extract_text_from_file(file_location)
    results = detect_personal_info(extracted_text)
    masked_text = mask_personal_info(extracted_text)

    # PDF 저장 경로 설정
    filename_wo_ext = os.path.splitext(file.filename)[0]
    pdf_path = f"app/static/{filename_wo_ext}_masked.pdf"
    save_masked_pdf(masked_text, pdf_path)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "filename": file.filename,
        "results": results,
        "total": len(results),
        "masked_text": masked_text,
        "pdf_path": f"/static/{filename_wo_ext}_masked.pdf"
    })

    
    
