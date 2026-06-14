from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.models.schemas import BookUploadResponse
from app.services.ocr_service import OCRService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
import shutil, uuid

router = APIRouter()
ocr = OCRService()
embedder = EmbeddingService()
store = VectorStore()

@router.post("/upload", response_model=BookUploadResponse)
async def upload_book(
    file: UploadFile = File(...),
    use_ocr: bool = Form(True)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "فقط PDF قبول میشه")

    book_id = str(uuid.uuid4())[:8]
    path = f"/app/uploads/{book_id}.pdf"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    pages = ocr.pdf_to_text_chunks(path, use_ocr=use_ocr)
    chunks = embedder.split_pages(pages)
    embeddings = await embedder.embed([c["text"] for c in chunks])

    store.create_collection(book_id)
    store.store_chunks(book_id, chunks, embeddings)

    return BookUploadResponse(
        book_id=book_id,
        pages_processed=len(pages),
        chunks_stored=len(chunks),
        message="کتاب با موفقیت پردازش شد"
    )