from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)
from app.core.qdrant import client
from app.services.embedding_service import (
    EmbeddingService,
)


class RetrieverService:

    COLLECTION = "books"

@classmethod
def search_lesson(
    cls,
    book: str,
    lesson: int,
    limit: int = 100,
):

    result = client.scroll(
        collection_name=cls.COLLECTION,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="book",
                    match=MatchValue(
                        value=book
                    ),
                ),
                FieldCondition(
                    key="lesson",
                    match=MatchValue(
                        value=lesson
                    ),
                ),
            ]
        ),
        limit=limit,
        with_payload=True,
    )

    chunks = []

    for point in result[0]:

        chunks.append(
            point.payload["text"]
        )

    return "\n".join(chunks)

    @classmethod
    def semantic_search(
        cls,
        query: str,
        limit: int = 10,
    ):

        vector = EmbeddingService.embed_query(
            query
        )

        result = client.search(
            collection_name=cls.COLLECTION,
            query_vector=vector,
            limit=limit,
            with_payload=True,
        )

        return [
            item.payload
            for item in result
        ]