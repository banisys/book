from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter(prefix="/books", tags=["Books"])

BOOKS_DIR = Path("storage/books")
BOOKS_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_book(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = BOOKS_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Book uploaded successfully",
        "filename": file.filename,
        "path": str(file_path)
    }