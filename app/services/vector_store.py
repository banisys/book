from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct
)
import uuid
import os

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=6333
        )

    def create_collection(self, book_id: str):
        self.client.recreate_collection(
            collection_name=book_id,
            vectors_config=VectorParams(
                size=1024,  # اندازه vector مدل BGE-M3
                distance=Distance.COSINE
            )
        )

    def store_chunks(self, book_id: str, chunks: list[dict], embeddings: list):
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"text": chunk["text"], "page": chunk["page"]}
            )
            for chunk, emb in zip(chunks, embeddings)
        ]
        self.client.upsert(collection_name=book_id, points=points)

    def search(self, book_id: str, query_vector: list, top_k: int = 5):
        return self.client.search(
            collection_name=book_id,
            query_vector=query_vector,
            limit=top_k
        )