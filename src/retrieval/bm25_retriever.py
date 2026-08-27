import json
import heapq
from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, json_path="outputs/processed_chunks.json"):

        print("Loading BM25 Retriever...")

        with open(json_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        self.corpus = [
            doc["text"].lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(self.corpus)

        print(f"Loaded {len(self.documents)} chunks into BM25.")

    def search(self, query, top_k=5):

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked = heapq.nlargest(
            top_k,
            zip(self.documents, scores),
            key=lambda x: x[1]
        )

        results = []

        for doc, score in ranked:

            results.append({

                "source": "BM25",

                "filename": doc.get("file_name", ""),

                "page": doc.get("page", "-"),

                "chunk_id": doc.get("chunk_id", ""),

                "score": float(score),

                "text": doc.get("text", "")

            })

        return results


if __name__ == "__main__":

    retriever = BM25Retriever()

    while True:

        query = input("\nAsk Oncology Question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        results = retriever.search(query)

        print("\n" + "=" * 100)

        for i, doc in enumerate(results, start=1):

            print(f"\nResult {i}")
            print(f"Source   : {doc['source']}")
            print(f"File     : {doc['filename']}")
            print(f"Page     : {doc['page']}")
            print(f"Chunk ID : {doc['chunk_id']}")
            print(f"Score    : {doc['score']:.4f}")
            print("-" * 100)
            print(doc["text"][:700])
            print("-" * 100)