from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import OncologyReranker
from src.llm.llama_client import LlamaClient

import time


class OncologyChatbot:

    def __init__(self):

        print("=" * 80)
        print("Initializing Oncology Agentic RAG")
        print("=" * 80)

        self.retriever = HybridRetriever()

        self.reranker = OncologyReranker()

        self.llm = LlamaClient()

        print("\nSystem Ready!")
        print("=" * 80)

    def build_prompt(self, query, documents):

        context = ""

        references = []

        for i, doc in enumerate(documents, start=1):

            context += (
                f"\n========== Evidence {i} ==========\n"
                f"Source : {doc['source']}\n"
                f"File   : {doc.get('filename','')}\n"
                f"Page   : {doc.get('page','-')}\n\n"
                f"{doc['text']}\n"
            )

            references.append(
                f"[{i}] {doc['source']} | "
                f"{doc.get('filename','')} | "
                f"Page {doc.get('page','-')}"
            )

        prompt = f"""
You are an expert oncology assistant.

Answer ONLY using the supplied evidence.

Instructions:

1. Do NOT hallucinate.

2. If evidence is insufficient, clearly state:
"The supplied evidence is insufficient."

3. Combine information from:

- Textbook
- PubMed
- Knowledge Graph
- BM25
- Qdrant

when available.

4. Write the answer in clear medical language.

5. At the end include a References section.

Evidence:

{context}

Question:

{query}

Answer:
"""

        return prompt, references

    def ask(self, query):

        start = time.time()

        # ---------------------------------------
        # Hybrid Retrieval
        # ---------------------------------------
        # ---------------------------------------
        # Hybrid Retrieval
        # ---------------------------------------
        documents = self.retriever.search(
            query,
            top_k=5
        )

        retrieval_time = time.time()

        # ---------------------------------------
        # CrossEncoder Reranking
        # ---------------------------------------
        reranked_docs = self.reranker.rerank(
            query,
            documents,
            top_k=8
        )

        rerank_time = time.time()

        # ---------------------------------------
        # Prompt
        # ---------------------------------------
        print("\n========== BUILDING PROMPT ==========")

        prompt, refs = self.build_prompt(
            query,
            reranked_docs
        )

        print("Prompt built successfully.")
        print("Prompt length:", len(prompt))

        # ---------------------------------------
        # LLM
        # ---------------------------------------
        print("\n========== CALLING LLM ==========")
        print("LLM object:", self.llm)

        print("\n========== BEFORE LLM ==========")

        answer = self.llm.generate(prompt)

        print("\n========== AFTER LLM ==========")
        print(answer)

        print("========== LLM RETURNED ==========")

        llm_time = time.time()

        print("\n")
        print("=" * 100)
        print("FINAL ANSWER")
        print("=" * 100)
        print(answer)

        print("\n")
        print("=" * 100)
        print("REFERENCES")
        print("=" * 100)

        for ref in refs:
            print(ref)

        print("\n")
        print("=" * 100)
        print("SYSTEM METRICS")
        print("=" * 100)

        print(f"Retrieval Time : {retrieval_time-start:.2f} sec")
        print(f"Reranking Time : {rerank_time-retrieval_time:.2f} sec")
        print(f"Generation Time: {llm_time-rerank_time:.2f} sec")
        print(f"Total Time     : {llm_time-start:.2f} sec")

        print("=" * 100)

        return {
    "question": query,

    "answer": answer,

    # Contexts required by RAGAS
    "contexts": [
        doc["text"] for doc in reranked_docs
    ],

    # Keep the documents also
    "documents": reranked_docs,

    "references": refs,

    "retrieval_time": retrieval_time - start,
    "reranking_time": rerank_time - retrieval_time,
    "generation_time": llm_time - rerank_time,
    "total_time": llm_time - start
}

if __name__ == "__main__":

    chatbot = OncologyChatbot()

    print("\n")
    print("=" * 80)
    print("Oncology Agentic RAG Chatbot")
    print("Type 'exit' to quit.")
    print("=" * 80)

    while True:

        query = input("\nAsk Oncology Question: ")

        if query.lower() in ["exit", "quit"]:

            print("\nGoodbye!")

            break

        chatbot.ask(query)