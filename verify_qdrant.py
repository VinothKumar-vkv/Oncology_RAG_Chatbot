from qdrant_client import QdrantClient

client = QdrantClient(path="vector_db")

info = client.get_collection("oncology_chunks")

print(info)