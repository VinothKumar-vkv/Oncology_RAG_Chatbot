from streamlit_agraph import (
    agraph,
    Config
)

from src.app.graph_utils import GraphUtils


class GraphViewer:

    def __init__(self):

        self.utils = GraphUtils()

    # =====================================================
    # Draw Knowledge Graph
    # =====================================================

    def draw(self, graph_docs):

        if not graph_docs:
            return

        # Build nodes and edges
        nodes, edges = self.utils.build_graph(graph_docs)

        config = Config(

            width=1000,

            height=650,

            directed=True,

            physics=True,

            hierarchical=False,

            nodeHighlightBehavior=True,

            highlightColor="#F7A7A6",

            collapsible=True,

            staticGraph=False,

            staticGraphWithDragAndDrop=False,

            fit=True

        )

        agraph(

            nodes=nodes,

            edges=edges,

            config=config

        )