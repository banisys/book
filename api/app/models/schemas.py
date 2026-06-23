from pydantic import BaseModel

class BookUploadResponse(BaseModel):
    book_id: str
    pages_processed: int
    chunks_stored: int
    message: str

class QueryRequest(BaseModel):
    book_id: str
    question: str
    max_chunks: int = 5

class QueryResponse(BaseModel):
    answer: str
    source_pages: list[int]


class AddTextRequest(BaseModel):
    book_id: str
    page: int
    text: str

class DeletePageRequest(BaseModel):
    book_id: str
    page: int