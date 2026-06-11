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
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.url, json={"texts": texts})
            return response.json()["embeddings"]

    def split_pages(self, pages: list[dict]) -> list[dict]:
        chunks = []
        for page in pages:
            splits = self.splitter.split_text(page["text"])
            for split in splits:
                if len(split.strip()) > 30:
                    chunks.append({
                        "text": split,
                        "page": page["page"]
                    })
        return chunks