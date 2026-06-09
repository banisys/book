from sentence_transformers import SentenceTransformer


class EmbeddingService:

    _model = None

    @classmethod
    def model(cls):

        if cls._model is None:

            cls._model = SentenceTransformer(
                "intfloat/multilingual-e5-large"
            )

        return cls._model

    @classmethod
    def embed_passage(
        cls,
        text: str,
    ):

        text = f"passage: {text}"

        return cls.model().encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    @classmethod
    def embed_query(
        cls,
        text: str,
    ):

        text = f"query: {text}"

        return cls.model().encode(
            text,
            normalize_embeddings=True,
        ).tolist()