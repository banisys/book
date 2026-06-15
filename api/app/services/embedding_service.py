import httpx
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

class EmbeddingService:
    def __init__(self):
        host = os.getenv("EMBEDDER_HOST", "embedder")
        self.url = f"http://{host}:8001/embed"
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", "،", " "]
        )

    async def embed(self, texts: list[str]) -> list[list[float]]:
        batch_size = 32
        all_embeddings = []

        async with httpx.AsyncClient(timeout=300) as client:
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = await client.post(self.url, json={"texts": batch})
                all_embeddings.extend(response.json()["embeddings"])

        return all_embeddings

    def split_pages(self, pages: list[dict]) -> list[dict]:
        chunks = []
        for page in pages:
            splits = self.splitter.split_text(page["text"])
            for split in splits:
                if len(split.strip()) > 5:  # از 30 به 5 تغییر کرد
                    chunks.append({
                        "text": split,
                        "page": page["page"]
                    })
        return chunks