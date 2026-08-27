import pickle
import numpy as np

from sentence_transformers import SentenceTransformer

from src.knowledge_graph.graph_retriever import GraphRetriever


class SemanticGraphRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-large-en-v1.5"
        )

        with open(
            "graph_embeddings.pkl",
            "rb"
        ) as f:

            self.names, self.embeddings = pickle.load(f)

        self.graph = GraphRetriever()

    def retrieve(self, entity):

        query_vector = self.model.encode(
            entity,
            normalize_embeddings=True
        )

        scores = np.dot(
            self.embeddings,
            query_vector
        )

        best = np.argmax(scores)

        matched_node = self.names[best]

        print(
            f"Matched '{entity}' → '{matched_node}'"
        )

        return self.graph.search(matched_node)
    
if __name__ == "__main__":

    retriever = SemanticGraphRetriever()

    while True:

        entity = input("\nEnter Entity (type 'exit' to quit): ")

        if entity.lower() == "exit":
            break

        results = retriever.retrieve(entity)

        print("\nRetrieved Graph Facts:\n")

        if not results:
            print("No graph facts found.")

        for r in results:
            print(r)