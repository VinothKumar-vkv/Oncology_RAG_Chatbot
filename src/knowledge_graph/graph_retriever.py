from src.knowledge_graph.neo4j_manager import Neo4jManager


class GraphRetriever:

    def __init__(self):

        self.neo4j = Neo4jManager()

    # ======================================================
    # Retrieve Graph Facts
    # ======================================================

    def search(self, entity, limit=20):

        query = """
        MATCH (a)-[r]->(b)

        WHERE toLower(a.name)=toLower($entity)

        RETURN

            a.name AS source,

            labels(a)[0] AS source_type,

            type(r) AS relation,

            b.name AS target,

            labels(b)[0] AS target_type

        LIMIT $limit
        """

        results = self.neo4j.execute(

            query,

            {

                "entity": entity,

                "limit": limit

            }

        )

        context = []

        for row in results:

            context.append(

                {

                    "source": "Knowledge Graph",

                    "page": "-",

                    "score": 1.0,

                    # -----------------------------
                    # Structured graph information
                    # -----------------------------
                    "source_node": row["source"],

                    "source_type": row["source_type"],

                    "relation": row["relation"],

                    "target_node": row["target"],

                    "target_type": row["target_type"],

                    # -----------------------------
                    # Human-readable text
                    # -----------------------------
                    "text":

                        f"{row['source']} "

                        f"{row['relation']} "

                        f"{row['target']}"

                }

            )

        return context

    # ======================================================
    # Close Neo4j
    # ======================================================

    def close(self):

        self.neo4j.close()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    retriever = GraphRetriever()

    while True:

        entity = input("\nEntity (type 'exit' to quit): ")

        if entity.lower() == "exit":
            break

        results = retriever.search(entity)

        print("\nRetrieved Graph Facts\n")

        if not results:

            print("No graph facts found.")

        else:

            for r in results:

                print(r)

    retriever.close()