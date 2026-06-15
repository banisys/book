from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.models.schemas import BookUploadResponse
from app.services.ocr_service import OCRService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
import shutil, uuid, json

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

    if not chunks:
        raise HTTPException(400, "متن کافی برای پردازش پیدا نشد")

    embeddings = await embedder.embed([c["text"] for c in chunks])
    embeddings = await embedder.embed([c["text"] for c in chunks])

    store.create_collection(book_id)
    store.store_chunks(book_id, chunks, embeddings)

    return BookUploadResponse(
        book_id=book_id,
        pages_processed=len(pages),
        chunks_stored=len(chunks),
        message="کتاب با موفقیت پردازش شد"
    )


@router.post("/upload-text", response_model=BookUploadResponse)
async def upload_text(
    file: UploadFile = File(...),
    book_id: str = Form(None)
):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".json"):
        data = json.loads(content.decode("utf-8"))
        if isinstance(data, list):
            pages = [
                {"page": i + 1,
                 "text": (p.get("text", "") if isinstance(p, dict) else str(p))}
                for i, p in enumerate(data)
            ]
        elif isinstance(data, dict):
            pages = [{"page": 1, "text": data.get("text", "")}]
        else:
            pages = [{"page": 1, "text": str(data)}]
    else:
        text = content.decode("utf-8")
        pages = [{"page": 1, "text": text}]

    # بررسی خالی نبودن
    if not any(p["text"].strip() for p in pages):
        raise HTTPException(400, "فایل خالی است")

    if not book_id:
        book_id = str(uuid.uuid4())[:8]

    chunks = embedder.split_pages(pages)
    embeddings = await embedder.embed([c["text"] for c in chunks])

    store.create_collection(book_id)
    store.store_chunks(book_id, chunks, embeddings)

    return BookUploadResponse(
        book_id=book_id,
        pages_processed=len(pages),
        chunks_stored=len(chunks),
        message="متن با موفقیت پردازش شد"
    )
