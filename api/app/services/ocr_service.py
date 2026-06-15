import fitz  # PyMuPDF
import io
import numpy as np
from PIL import Image

class OCRService:
    def __init__(self):
        self._reader = None

    def _load_reader(self):
        """lazy load — فقط اولین بار لود میشه"""
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(['fa', 'en'], gpu=False)
        return self._reader

    def _extract_with_easyocr(self, image: Image.Image) -> str:
        reader = self._load_reader()
        img_array = np.array(image)
        results = reader.readtext(img_array)

        # مرتب‌سازی از بالا به پایین بر اساس موقعیت y
        results.sort(key=lambda x: x[0][0][1])

        # فقط نتایج با confidence بالای 0.3 رو نگه دار
        lines = [text for _, text, conf in results if conf > 0.3]
        return "\n".join(lines)

    def _extract_direct(self, page) -> str:
        """استخراج مستقیم متن از لایه PDF"""
        return page.get_text()

    def pdf_to_text_chunks(self, pdf_path: str, use_ocr: bool = True) -> list[dict]:
        """
        use_ocr=True  -> EasyOCR (برای PDF با متن خراب)
        use_ocr=False -> استخراج مستقیم از لایه متنی PDF
        """
        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            if use_ocr:
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                text = self._extract_with_easyocr(image)
            else:
                text = self._extract_direct(page)

            if text.strip():
                pages.append({
                    "page": page_num + 1,
                    "text": text.strip()
                })

        doc.close()
        return pages