from sentence_transformers import CrossEncoder


class OncologyReranker:

    def __init__(self):

        print("Loading BAAI Reranker...")

        self.model = CrossEncoder("BAAI/bge-reranker-base")

        print("Reranker Loaded Successfully!")

    def rerank(self, query, retrieved_docs, top_k=5):

        if not retrieved_docs:
            return []

        valid_docs = []

        for doc in retrieved_docs:

            if (
                isinstance(doc, dict)
                and doc.get("text")
                and doc["text"].strip()
            ):
                valid_docs.append(doc)

        if not valid_docs:
            return []

        pairs = [
            (query, doc["text"])
            for doc in valid_docs
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for doc, score in zip(valid_docs, scores):

            doc = doc.copy()
            doc["rerank_score"] = float(score)

            reranked.append(doc)

        reranked = sorted(
            reranked,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:top_k]


if __name__ == "__main__":

    from src.retrieval.hybrid_retriever import HybridRetriever

    retriever = HybridRetriever()

    reranker = OncologyReranker()

    while True:

        query = input("\nAsk Oncology Question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        docs = retriever.search(query)

        results = reranker.rerank(query, docs)

        print("\n" + "=" * 100)

        for i, doc in enumerate(results, start=1):

            print(f"\nResult {i}")
            print(f"Source        : {doc['source']}")
            print(f"File          : {doc.get('filename', '')}")
            print(f"Page          : {doc['page']}")
            print(f"Chunk ID      : {doc['chunk_id']}")
            print(f"Search Score  : {doc['score']:.4f}")
            print(f"Rerank Score  : {doc['rerank_score']:.4f}")

            print("-" * 100)

            print(doc["text"][:700])

            print("-" * 100)