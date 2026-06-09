from fastapi import APIRouter

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/")
async def generate_quiz(payload: dict):
    """
    نمونه ورودی:

    {
        "book":"math8",
        "lesson":5,
        "count":5
    }
    """

    return {
        "book": payload.get("book"),
        "lesson": payload.get("lesson"),
        "count": payload.get("count"),
        "questions": []
    }