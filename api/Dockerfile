FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fas \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/ggml-org/llama.cpp/releases/download/b5570/llama-b5570-bin-ubuntu-x64.zip \
    -o /tmp/llama.zip && \
    unzip /tmp/llama.zip -d /tmp/llama && \
    mv /tmp/llama/build/bin/llama-server /usr/local/bin/llama-server && \
    chmod +x /usr/local/bin/llama-server && \
    rm -rf /tmp/llama /tmp/llama.zip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 --upgrade pip && \
    pip install --no-cache-dir --timeout=300 -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]