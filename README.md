
docker-compose up --build


curl -X POST http://localhost:8000/books/upload \
  -F "file=@ketab.pdf"


curl -X POST http://localhost:8000/query/ask \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "abc12345",
    "question": "درس سوم را در ۳ پاراگراف خلاصه کن"
  }'