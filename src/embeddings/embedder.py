import json
from sentence_transformers import SentenceTransformer

from pathlib import Path

import sys

sys.path.append("src")

from config.settings import *


class Embedder:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def load_chunks(self):

        with open(CHUNK_FILE, encoding="utf-8") as f:

            return json.load(f)

    def embed(self):

        chunks = self.load_chunks()

        texts = [c["text"] for c in chunks]

        print(f"Generating embeddings for {len(texts)} chunks...")

        vectors = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=BATCH_SIZE,
            normalize_embeddings=True
        )

        for chunk, vector in zip(chunks, vectors):

            chunk["embedding"] = vector.tolist()

        Path("outputs").mkdir(exist_ok=True)

        with open(
            "outputs/embedded_chunks.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chunks,
                f,
                ensure_ascii=False
            )

        print()

        print("Embeddings Saved")

        print(f"Total : {len(chunks)}")


if __name__ == "__main__":

    Embedder().embed()