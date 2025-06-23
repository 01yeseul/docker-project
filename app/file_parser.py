import fitz  # PyMuPDF
from docx import Document
import os
from PIL import Image
import pytesseract


def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".txt":
        return _extract_txt(file_path)
    elif ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext == ".docx":
        return _extract_docx(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return _extract_image(file_path)
    else:
        return "지원하지 않는 파일 형식입니다."


def _extract_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_pdf(file_path: str) -> str:
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def _extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def _extract_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='kor+eng')  # 한글+영어 지원
        return text
    except Exception as e:
        return f"OCR 오류: {e}"
