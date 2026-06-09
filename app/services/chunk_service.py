import re


class ChunkService:

    LESSON_PATTERN = r"(درس\s+\d+.*?)((?=درس\s+\d+)|$)"

    @classmethod
    def split_lessons(cls, text: str):
        matches = re.findall(
            cls.LESSON_PATTERN,
            text,
            re.DOTALL
        )

        lessons = []

        lesson_number = 0

        for lesson_title, lesson_content in matches:

            lesson_number += 1

            lessons.append(
                {
                    "lesson": lesson_number,
                    "title": lesson_title.split("\n")[0].strip(),
                    "content": lesson_title + lesson_content,
                }
            )

        return lessons

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += chunk_size - overlap

        return chunks

    @classmethod
    def prepare_chunks(
        cls,
        lessons,
        book_name: str,
    ):
        output = []

        for lesson in lessons:

            chunks = cls.chunk_text(
                lesson["content"]
            )

            for index, chunk in enumerate(chunks):

                output.append(
                    {
                        "book": book_name,
                        "lesson": lesson["lesson"],
                        "title": lesson["title"],
                        "chunk_index": index,
                        "text": chunk,
                    }
                )

        return output