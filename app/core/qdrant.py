from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
)

client = QdrantClient(
    host="qdrant",
    port=6333,
)

COLLECTION_NAME = "books"


def create_collection():

    collections = client.get_collections()

    exists = any(
        c.name == COLLECTION_NAME
        for c in collections.collections
    )

    if exists:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE,
        ),
    )