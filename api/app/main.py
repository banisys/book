from fastapi import FastAPI
from api.app.routers import books
from api.app.routers import query

app = FastAPI(title="Book Service", description="سرویس پردازش کتاب درسی")

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(query.router, prefix="/query", tags=["query"])

@app.get("/health")
def health():
    return {"status": "ok"}