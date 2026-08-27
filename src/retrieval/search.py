from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
COLLECTION_NAME = "oncology_chunks"


class OncologySearcher:

    def __init__(self):

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.client = QdrantClient(path="vector_db")

    def search(self, query, top_k=5):

        query_vector = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k
        )

        docs = []

        for point in results.points:

            payload = point.payload

            docs.append({

                "source": "Qdrant",

                "page": payload.get("page", "-"),

                "score": float(point.score),

                "text": payload.get("text", ""),

                "filename": payload.get("filename", ""),

                "chunk_id": payload.get("chunk_id", "")
            })

        return docs