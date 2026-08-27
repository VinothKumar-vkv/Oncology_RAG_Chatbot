from src.vectorstore.qdrant_manager import QdrantManager

manager = QdrantManager()

manager.upload_embeddings("outputs/embedded_chunks.json")