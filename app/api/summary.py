from fastapi import APIRouter

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.post("/")
async def summarize(payload: dict):
    """
    نمونه ورودی:

    {
        "book":"math8",
        "lesson":5,
        "paragraphs":3
    }
    """

    return {
        "book": payload.get("book"),
        "lesson": payload.get("lesson"),
        "paragraphs": payload.get("paragraphs"),
        "summary": "Not implemented yet"
    }