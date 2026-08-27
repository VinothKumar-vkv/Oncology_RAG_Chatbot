from datetime import datetime


class MetadataGenerator:

    @staticmethod
    def create(
        chunk_id,
        filename,
        page,
        chunk,
        chunk_index
    ):

        return {
            "chunk_id": chunk_id,
            "chunk_index": chunk_index,
            "file_name": filename,
            "page": page,
            "word_count": len(chunk.split()),
            "character_count": len(chunk),
            "created_at": datetime.now().isoformat(),
            "text": chunk
        }