import requests

from app.services.retriever_service import (
    RetrieverService,
)


class SummaryService:

    OLLAMA_URL = (
        "http://ollama:11434/api/generate"
    )

    MODEL = "qwen2.5:7b"

    @classmethod
    def summarize(
        cls,
        lesson: int,
        paragraphs: int = 3,
    ):

        context = (
            RetrieverService.search_lesson(
                book="math8",
                lesson=5,
            )
        )

        prompt = f"""
تو یک معلم باتجربه هستی.

فقط از متن زیر استفاده کن.

متن:

{context}

درس را در {paragraphs} پاراگراف
خلاصه کن.
"""

        response = requests.post(
            cls.OLLAMA_URL,
            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        return response.json()["response"]