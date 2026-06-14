import fitz  # PyMuPDF
import io
import re
from PIL import Image

class OCRService:
    def __init__(self):
        self._predictor = None

    def _load_predictor(self):
        """lazy load — فقط اولین بار لود میشه"""
        if self._predictor is None:
            from surya.inference import SuryaInferenceManager
            from surya.recognition import RecognitionPredictor
            manager = SuryaInferenceManager()
            self._predictor = RecognitionPredictor(manager)
        return self._predictor

    def _html_to_text(self, html: str) -> str:
        """تگ‌های HTML رو حذف کن و متن خالص بگیر"""
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_with_surya(self, image: Image.Image) -> str:
        predictor = self._load_predictor()
        results = predictor([image], full_page=True)
        page = results[0]

        blocks = sorted(
            [b for b in page.blocks if not b.skipped and not b.error and b.html],
            key=lambda b: b.reading_order
        )
        return "\n".join([self._html_to_text(b.html) for b in blocks])

    def _extract_direct(self, page) -> str:
        return page.get_text()

    def pdf_to_text_chunks(self, pdf_path: str, use_ocr: bool = True) -> list[dict]:
        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            if use_ocr:
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                text = self._extract_with_surya(image)
            else:
                text = self._extract_direct(page)

            if text.strip():
                pages.append({
                    "page": page_num + 1,
                    "text": text.strip()
                })

        doc.close()
        return pages