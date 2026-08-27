import uuid
import ijson
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

COLLECTION_NAME = "oncology_chunks"
EMBEDDING_DIM = 1024      # Change if your embedding model uses a different size
BATCH_SIZE = 500


class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(path="vector_db")

    def create_collection(self):
        collections = [c.name for c in self.client.get_collections().collections]

        if COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {COLLECTION_NAME}")
        else:
            print(f"Collection already exists: {COLLECTION_NAME}")

    def upload_embeddings(self, json_file):
        self.create_collection()

        batch = []
        total = 0

        with open(json_file, "rb") as f:
            parser = ijson.items(f, "item")

            for chunk in parser:
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=chunk["embedding"],
                    payload={
                        "chunk_id": chunk["chunk_id"],
                        "file_name": chunk["file_name"],
                        "page": chunk["page"],
                        "text": chunk["text"],
                    },
                )

                batch.append(point)

                if len(batch) >= BATCH_SIZE:
                    self.client.upsert(
                        collection_name=COLLECTION_NAME,
                        points=batch,
                    )

                    total += len(batch)
                    print(f"Uploaded {total} vectors...")
                    batch = []

            if batch:
                self.client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=batch,
                )

                total += len(batch)

        print(f"\nDone! Uploaded {total} vectors.")