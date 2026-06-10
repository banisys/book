from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('BAAI/bge-m3')
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", "،", " "]
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

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