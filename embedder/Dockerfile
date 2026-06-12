FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --timeout=300 sentence-transformers fastapi uvicorn

RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('BAAI/bge-m3'); model.save('/app/bge-m3')"

COPY server.py .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]