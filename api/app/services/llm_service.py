import httpx
import os

class LLMService:
    def __init__(self):
        host = os.getenv("OLLAMA_HOST", "localhost")
        self.base_url = f"http://{host}:11434"
        self.model = os.getenv("LLM_MODEL", "qwen2.5:7b")

    async def generate(self, context: str, question: str) -> str:
        prompt = f"""تو یک دستیار آموزشی هستی. بر اساس متن زیر از کتاب درسی، به سوال پاسخ بده.

متن کتاب:
{context}

سوال: {question}

پاسخ را به زبان فارسی و به صورت واضح بنویس:"""

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                }
            )
            data = response.json()
            return data["response"]