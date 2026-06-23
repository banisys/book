from fastapi import APIRouter, HTTPException
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
import uuid
from app.models.schemas import AddTextRequest
from app.models.schemas import DeletePageRequest

router = APIRouter()

embedder = EmbeddingService()
store = VectorStore()

@router.post("/create")
async def create_book():
    book_id = str(uuid.uuid4())[:8]
    store.create_collection(book_id)
    return {"book_id": book_id, "message": "کتاب خالی ایجاد شد"}


@router.post("/add-text")
async def add_text(req: AddTextRequest):
    chunks = embedder.split_pages([{"page": req.page, "text": req.text}])

    if not chunks:
        raise HTTPException(400, "متن کافی برای پردازش پیدا نشد")

    embeddings = await embedder.embed([c["text"] for c in chunks])
    store.store_chunks(req.book_id, chunks, embeddings)

    return {
        "book_id": req.book_id,
        "page": req.page,
        "chunks_stored": len(chunks),
        "message": "متن ذخیره شد"
    }



@router.delete("/delete-page")
async def delete_page(request: DeletePageRequest):
    deleted = store.delete_by_page(
        request.book_id,
        request.page
    )

    return {
        "book_id": request.book_id,
        "page": request.page,
        "deleted": deleted,
        "message": "صفحه حذف شد"
    }