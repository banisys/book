import fitz


class PDFService:

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        doc = fitz.open(pdf_path)

        pages = []

        for page in doc:
            text = page.get_text()
            if text:
                pages.append(text)

        doc.close()

        return "\n".join(pages)