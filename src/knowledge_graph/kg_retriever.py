from neo4j import GraphDatabase


class Neo4jRetriever:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "haritha123")
        )

    def search(self, query, top_k=10):

        cypher = """
        MATCH (a)-[r]->(b)

        WHERE
            toLower(a.name) CONTAINS toLower($query)
            OR
            toLower(b.name) CONTAINS toLower($query)

        RETURN
            labels(a)[0] AS source_type,
            a.name AS source,
            type(r) AS relation,
            labels(b)[0] AS target_type,
            b.name AS target

        LIMIT $top_k
        """

        with self.driver.session() as session:

            result = session.run(
    cypher,
    {
        "query": query,
        "top_k": top_k
    }
)
            docs = []

            for row in result:

                docs.append({

                    "source": "KnowledgeGraph",

                    "filename": "Neo4j",

                    "page": "-",

                    "chunk_id": "-",

                    "score": 1.0,

                    "text":
                    f"{row['source_type']}: {row['source']} "
                    f"--{row['relation']}--> "
                    f"{row['target_type']}: {row['target']}"

                })

        return docs