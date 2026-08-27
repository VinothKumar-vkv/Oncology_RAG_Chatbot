from sentence_transformers import SentenceTransformer
from src.knowledge_graph.neo4j_manager import Neo4jManager
import pickle


class GraphIndexer:

    def __init__(self):

        self.neo4j = Neo4jManager()

        self.model = SentenceTransformer(
            "BAAI/bge-large-en-v1.5"
        )

    def build(self):

        query = """
        MATCH (n)
        RETURN DISTINCT n.name AS name
        """

        nodes = self.neo4j.execute(query)

        names = [
            row["name"]
            for row in nodes
        ]

        embeddings = self.model.encode(
            names,
            normalize_embeddings=True
        )

        with open(
            "graph_embeddings.pkl",
            "wb"
        ) as f:

            pickle.dump(
                (names, embeddings),
                f
            )

        print(f"Indexed {len(names)} graph nodes.")


if __name__ == "__main__":

    GraphIndexer().build()