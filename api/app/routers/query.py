from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService

router = APIRouter()
embedder = EmbeddingService()
store = VectorStore()
llm = LLMService()

@router.post("/ask", response_model=QueryResponse)
async def ask(req: QueryRequest):
    print('ddd')
    try:
        q_vec = (await embedder.embed([req.question]))[0]
        results = store.search(req.book_id, q_vec, req.max_chunks)

        if not results:
            raise HTTPException(404, "محتوایی پیدا نشد")

        context = "\n\n".join([r.payload["text"] for r in results])
        pages = list(set([r.payload["page"] for r in results]))

        answer = await llm.generate(context, req.question)

        return QueryResponse(answer=answer, source_pages=sorted(pages))
    except Exception as e:
        raise HTTPException(500, str(e))