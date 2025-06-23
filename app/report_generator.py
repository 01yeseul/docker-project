from fpdf import FPDF
import os

FONT_PATH = "app/fonts/Pretendard-Regular.ttf"
FONT_NAME = "Pretendard"

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()

        # 한글 폰트 등록 (Unicode=True)
        self.add_font(FONT_NAME, '', FONT_PATH, uni=True)
        self.set_font(FONT_NAME, size=12)

    def add_masked_text(self, text: str):
        lines = text.split("\n")
        for line in lines:
            self.multi_cell(0, 10, line)

def save_masked_pdf(text: str, output_path: str):
    pdf = PDF()
    pdf.add_masked_text(text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
