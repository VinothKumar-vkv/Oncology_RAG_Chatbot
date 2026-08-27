import json

from src.knowledge_graph.neo4j_manager import Neo4jManager
from src.knowledge_graph.relationship_extractor import RelationshipExtractor
from src.knowledge_graph.entity_normalizer import EntityNormalizer
from src.knowledge_graph.relationship_validator import RelationshipValidator


class GraphBuilder:

    def __init__(self):

        self.neo4j = Neo4jManager()

        self.extractor = RelationshipExtractor()

        self.normalizer = EntityNormalizer()

        self.validator = RelationshipValidator()

    def build(self, text):

        # Skip empty chunk
        if not text.strip():
            return 0

        # Extract relationships
        response = self.extractor.extract(text)

        try:

            triples = json.loads(response)

        except Exception:

            print("\nInvalid JSON returned by Llama")
            print(response)

            return 0

        if len(triples) == 0:
            return 0

        inserted = 0

        seen = set()

        for triple in triples:

            try:

                source = self.normalizer.normalize(
                    triple["source"].strip()
                )

                target = self.normalizer.normalize(
                    triple["target"].strip()
                )

                source_type = triple["source_type"].strip()

                target_type = triple["target_type"].strip()

                relation = triple["relation"].strip()

                # -----------------------------
                # Skip empty entities
                # -----------------------------
                if source == "" or target == "":
                    continue

                # -----------------------------
                # Skip self relationships
                # -----------------------------
                if source.lower() == target.lower():
                    continue

                # -----------------------------
                # Validate relationship
                # -----------------------------
                if not self.validator.is_valid(
                    source_type,
                    relation,
                    target_type
                ):
                    continue

                # -----------------------------
                # Remove duplicate triples
                # -----------------------------
                key = (
                    source.lower(),
                    relation,
                    target.lower()
                )

                if key in seen:
                    continue

                seen.add(key)

                # -----------------------------
                # Insert into Neo4j
                # -----------------------------
                query = f"""
                MERGE (a:{source_type} {{name:$source}})
                MERGE (b:{target_type} {{name:$target}})
                MERGE (a)-[:{relation}]->(b)
                """

                self.neo4j.execute(
                    query,
                    {
                        "source": source,
                        "target": target
                    }
                )

                inserted += 1

            except Exception as e:

                print("\nSkipped one relationship")

                print(e)

        return inserted

    def close(self):

        self.neo4j.close()


if __name__ == "__main__":

    builder = GraphBuilder()

    sample = """
    HER2 positive breast cancer is commonly treated with trastuzumab.

    BRCA1 mutation increases breast cancer risk.

    HER2 protein is overexpressed in HER2 positive breast cancer.

    Trastuzumab targets HER2.

    HER2 positive breast cancer responds to trastuzumab.

    """

    count = builder.build(sample)

    print(f"\nInserted {count} relationships.")

    builder.close()