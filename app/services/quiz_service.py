import json
import requests

from app.services.retriever_service import (
    RetrieverService,
)


class QuizService:

    OLLAMA_URL = (
        "http://ollama:11434/api/generate"
    )

    MODEL = "qwen2.5:7b"

    @classmethod
    def generate(
        cls,
        book: str,
        lesson: int,
        count: int = 5,
    ):

        context = (
            RetrieverService.search_lesson(
                book=book,
                lesson=lesson,
            )
        )

        if not context.strip():
            return {
                "error": "Lesson not found"
            }

        prompt = f"""
تو یک معلم باتجربه هستی.

فقط و فقط از محتوای زیر استفاده کن.

متن درس:

{context}

{count} سوال چهار گزینه‌ای طراحی کن.

قوانین:

- هر سوال فقط یک پاسخ صحیح داشته باشد.
- سوال‌ها از متن درس باشند.
- گزینه‌ها تکراری نباشند.
- سطح سوال‌ها متوسط باشد.
- پاسخ صحیح را مشخص کن.

خروجی را فقط به صورت JSON برگردان.

فرمت خروجی:

[
  {{
    "question": "متن سوال",
    "options": [
      "گزینه 1",
      "گزینه 2",
      "گزینه 3",
      "گزینه 4"
    ],
    "answer": 1
  }}
]
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

        content = response.json()[
            "response"
        ].strip()

        try:

            return json.loads(
                content
            )

        except json.JSONDecodeError:

            return {
                "error":
                    "Model returned invalid JSON",
                "raw_response":
                    content,
            }