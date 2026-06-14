import fitz  # PyMuPDF
import io
from PIL import Image

class OCRService:
    def __init__(self):
        self._surya_models = None

    def _load_surya(self):
        """lazy load — فقط اولین بار که نیاز باشه لود میشه"""
        if self._surya_models is None:
            from surya.model.detection.model import load_model as load_det_model
            from surya.model.detection.model import load_processor as load_det_processor
            from surya.model.recognition.model import load_model as load_rec_model
            from surya.model.recognition.processor import load_processor as load_rec_processor

            self._surya_models = {
                "det_model": load_det_model(),
                "det_processor": load_det_processor(),
                "rec_model": load_rec_model(),
                "rec_processor": load_rec_processor(),
            }
        return self._surya_models

    def _extract_with_surya(self, image: Image.Image) -> str:
        from surya.ocr import run_ocr

        models = self._load_surya()
        predictions = run_ocr(
            [image],
            [["fa", "en"]],
            models["det_model"],
            models["det_processor"],
            models["rec_model"],
            models["rec_processor"],
        )
        lines = predictions[0].text_lines
        # مرتب‌سازی از بالا به پایین
        lines.sort(key=lambda x: x.bbox[1])
        return "\n".join([line.text for line in lines if line.text.strip()])

    def _extract_direct(self, page) -> str:
        """استخراج مستقیم متن از لایه PDF"""
        return page.get_text()

    def pdf_to_text_chunks(self, pdf_path: str, use_ocr: bool = True) -> list[dict]:
        """
        use_ocr=True  -> surya OCR (برای PDF با متن خراب)
        use_ocr=False -> استخراج مستقیم از لایه متنی PDF
        """
        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            if use_ocr:
                # رزولوشن بالا برای OCR بهتر
                mat = fitz.Matrix(2.0, 2.0)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
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