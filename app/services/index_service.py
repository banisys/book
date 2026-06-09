import uuid
from pathlib import Path

from qdrant_client.models import (
    PointStruct,
)

from app.core.qdrant import client
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.embedding_service import (
    EmbeddingService,
)


class IndexService:

    COLLECTION = "books"

    @classmethod
    def index_book(
        cls,
        pdf_path: str,
    ):

        book_name = Path(
            pdf_path
        ).stem

        text = PDFService.extract_text(
            pdf_path
        )

        lessons = ChunkService.split_lessons(
            text
        )

        chunks = ChunkService.prepare_chunks(
            lessons,
            book_name,
        )

        points = []

        for chunk in chunks:

            embedding = (
                EmbeddingService.embed_passage(
                    chunk["text"]
                )
            )

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "book": chunk["book"],
                        "lesson": chunk["lesson"],
                        "title": chunk["title"],
                        "chunk_index":
                            chunk["chunk_index"],
                        "text": chunk["text"],
                    },
                )
            )

        batch_size = 100

        for i in range(
            0,
            len(points),
            batch_size,
        ):

            batch = points[
                i:i + batch_size
            ]

            client.upsert(
                collection_name=cls.COLLECTION,
                points=batch,
                wait=True,
            )

        return {
            "book": book_name,
            "lessons": len(lessons),
            "chunks": len(chunks),
        }