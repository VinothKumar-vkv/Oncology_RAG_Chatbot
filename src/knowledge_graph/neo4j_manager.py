from neo4j import GraphDatabase


class Neo4jManager:

    def __init__(self):

        self.uri = "bolt://localhost:7687"

        self.username = "neo4j"

        self.password = "haritha123"

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def close(self):
        self.driver.close()

    def execute(self, query, parameters=None):

        with self.driver.session() as session:

            if parameters is None:
                parameters = {}

            result = session.run(query, parameters)

            return [record.data() for record in result]


if __name__ == "__main__":

    graph = Neo4jManager()

    graph.execute(
        """
        CREATE (:Test {name:"Connected Successfully"})
        """
    )

    print("Neo4j Connected!")

    graph.close()