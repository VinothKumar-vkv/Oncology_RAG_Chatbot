from streamlit_agraph import Node, Edge


class GraphUtils:

    def __init__(self):

        self.node_colors = {

            "Cancer": "#E53935",
            "Disease": "#FB8C00",
            "Drug": "#43A047",
            "Gene": "#1E88E5",
            "Biomarker": "#8E24AA",
            "Protein": "#FDD835",
            "Treatment": "#00897B",
            "Procedure": "#6D4C41",
            "Organ": "#546E7A",
            "Symptom": "#EC407A",
            "Mutation": "#5E35B1",
            "Pathway": "#3949AB",
            "Unknown": "#90A4AE"
        }

    # ======================================================
    # Get node color
    # ======================================================

    def get_color(self, node_type):

        return self.node_colors.get(
            node_type,
            self.node_colors["Unknown"]
        )

    # ======================================================
    # Build Streamlit Graph
    # ======================================================

    def build_graph(self, graph_docs):

        nodes = []
        edges = []

        node_ids = set()
        edge_ids = set()

        for doc in graph_docs:

            # --------------------------------------------
            # Skip invalid documents
            # --------------------------------------------

            if not isinstance(doc, dict):
                continue

            source = doc.get("source_node")

            target = doc.get("target_node")

            relation = doc.get("relation")

            source_type = doc.get(
                "source_type",
                "Unknown"
            )

            target_type = doc.get(
                "target_type",
                "Unknown"
            )

            if source is None or target is None or relation is None:
                continue

            # --------------------------------------------
            # Source Node
            # --------------------------------------------

            if source not in node_ids:

                nodes.append(

                    Node(

                        id=source,

                        label=source,

                        size=35,

                        color=self.get_color(
                            source_type
                        )

                    )

                )

                node_ids.add(source)

            # --------------------------------------------
            # Target Node
            # --------------------------------------------

            if target not in node_ids:

                nodes.append(

                    Node(

                        id=target,

                        label=target,

                        size=28,

                        color=self.get_color(
                            target_type
                        )

                    )

                )

                node_ids.add(target)

            # --------------------------------------------
            # Edge
            # --------------------------------------------

            edge_key = (
                source,
                relation,
                target
            )

            if edge_key not in edge_ids:

                edges.append(

                    Edge(

                        source=source,

                        target=target,

                        label=relation

                    )

                )

                edge_ids.add(edge_key)

        return nodes, edges