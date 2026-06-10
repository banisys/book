import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

class OCRService:
    def __init__(self):
        self.config = "--oem 3 --psm 3 -l fas"  # فارسی

    def pdf_to_text_chunks(self, pdf_path: str) -> list[dict]:
        """هر صفحه PDF رو به تصویر تبدیل کرده و OCR میزنه"""
        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            # رزولوشن بالا برای OCR بهتر
            mat = fitz.Matrix(2.5, 2.5)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")

            image = Image.open(io.BytesIO(img_data))
            text = pytesseract.image_to_string(image, config=self.config)

            if text.strip():
                pages.append({
                    "page": page_num + 1,
                    "text": text.strip()
                })

        doc.close()
        return pages