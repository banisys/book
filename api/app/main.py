from fastapi import FastAPI
from app.routers import books, query

app = FastAPI(title="Book Service", description="سرویس پردازش کتاب درسی")

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(query.router, prefix="/query", tags=["query"])
