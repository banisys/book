from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.qdrant import (
    create_collection,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_collection()

    yield


app = FastAPI(
    title="School Books RAG",
    lifespan=lifespan,
)