from src.retrieval.search import OncologySearcher
from src.retrieval.bm25_retriever import BM25Retriever
from src.mcp.pubmed_client import PubMedMCPClient
from src.knowledge_graph.kg_retriever import Neo4jRetriever
import asyncio
import json

class HybridRetriever:

    def __init__(self):

        print("Loading Hybrid Retriever...")

        self.kg = Neo4jRetriever()

        self.qdrant = OncologySearcher()
        self.bm25 = BM25Retriever()
        self.pubmed = PubMedMCPClient()

        print("Hybrid Retriever Ready!")

    def search(self, query, top_k=5):

        # ==========================
        # Dense Retrieval (Qdrant)
        # ==========================
        dense_results = self.qdrant.search(
            query,
            top_k=top_k
        )

        # ==========================
        # Sparse Retrieval (BM25)
        # ==========================
        sparse_results = self.bm25.search(
            query,
            top_k=top_k
        )

        kg_results = self.kg.search(
    query,
    top_k=top_k
)

        # ==========================
        # PubMed Retrieval
        # ==========================
        # PubMed disabled for WITHOUT MCP experiment
        pubmed_results = []

        combined = []
        seen = set()

        # ==========================
        # Qdrant Results
        # ==========================
        for result in dense_results:

            text = result.get("text", "").strip()

            if not text or text in seen:
                continue

            combined.append({
                "source": "Qdrant",
                "filename": result.get("filename", ""),
                "page": result.get("page", "-"),
                "chunk_id": result.get("chunk_id", ""),
                "score": float(result.get("score", 0)),
                "text": text
            })

            seen.add(text)

        # ==========================
        # BM25 Results
        # ==========================
        for result in sparse_results:

            text = result.get("text", "").strip()

            if not text or text in seen:
                continue

            combined.append({
                "source": "BM25",
                "filename": result.get("filename", ""),
                "page": result.get("page", "-"),
                "chunk_id": result.get("chunk_id", ""),
                "score": float(result.get("score", 0)),
                "text": text
            })

            seen.add(text)
        # ==========================
        # Knowledge Graph Results
        # ==========================
        for result in kg_results:

            text = result.get("text", "").strip()

            if not text or text in seen:
                continue

            combined.append({
                "source": "KnowledgeGraph",
                "filename": result.get("filename", "Neo4j"),
                "page": result.get("page", "-"),
                "chunk_id": result.get("chunk_id", "-"),
                "score": float(result.get("score", 1.0)),
                "text": text
            })

            seen.add(text)

        # ==========================
        # PubMed Results
        # ==========================
        # ==========================
        # PubMed Results
        # ==========================
        # ==========================
        # PubMed Disabled
        # ==========================
        # WITHOUT MCP experiment
        pass
        # =====================================
        # IMPORTANT:
        # Do NOT sort here.
        # Let the CrossEncoder reranker decide
        # the final ranking.
        # =====================================

                # =====================================
        # IMPORTANT:
        # Do NOT sort here.
        # Let the CrossEncoder reranker decide
        # the final ranking.
        # =====================================

        print("\n========== RETRIEVAL DEBUG ==========")

        for i, doc in enumerate(combined, start=1):

            print(f"\nResult {i}")
            print(f"Source   : {doc['source']}")
            print(f"Filename : {doc['filename']}")
            print(f"Page     : {doc['page']}")
            print(f"Chunk ID : {doc['chunk_id']}")
            print(f"Score    : {doc['score']:.4f}")
            print(f"Text     : {doc['text'][:150]}")

        print("\n=====================================\n")

        return combined


if __name__ == "__main__":

    from src.retrieval.reranker import OncologyReranker

    retriever = HybridRetriever()

    reranker = OncologyReranker()

    while True:

        query = input("\nAsk Oncology Question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        docs = retriever.search(query)

        results = reranker.rerank(
            query,
            docs,
            top_k=8
        )

        print("\n" + "=" * 100)

        for i, doc in enumerate(results, start=1):

            print(f"\nResult {i}")
            print(f"Source        : {doc['source']}")
            print(f"File          : {doc.get('filename', '')}")
            print(f"Page          : {doc['page']}")
            print(f"Chunk ID      : {doc['chunk_id']}")

            if "score" in doc:
                print(f"Search Score  : {doc['score']:.4f}")

            print(f"Rerank Score  : {doc['rerank_score']:.4f}")

            print("-" * 100)
            print(doc["text"][:700])
            print("-" * 100)