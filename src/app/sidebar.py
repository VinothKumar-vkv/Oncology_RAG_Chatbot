import streamlit as st


def render_sidebar(stats=None):
    """
    Renders the application sidebar.

    Parameters
    ----------
    stats : dict
        {
            "question_type": "...",
            "chunks": 0,
            "pubmed": 0,
            "graph": 0,
            "time": 0
        }
    """

    with st.sidebar:

        st.title("🩺 Oncology Agent")

        st.markdown("---")

        # ======================================
        # Retrieval Sources
        # ======================================

        st.subheader("📚 Retrieval Sources")

        pdf_enabled = st.checkbox(
            "Medical Textbook",
            value=True
        )

        pubmed_enabled = st.checkbox(
            "PubMed",
            value=True
        )

        graph_enabled = st.checkbox(
            "Knowledge Graph",
            value=True
        )

        st.markdown("---")

        # ======================================
        # Statistics
        # ======================================

        st.subheader("📊 Retrieval Statistics")

        if stats is None:

            st.info("Ask a question to view statistics.")

        else:

            st.metric(
                "Question Type",
                stats.get("question_type", "-")
            )

            st.metric(
                "PDF Chunks",
                stats.get("chunks", 0)
            )

            st.metric(
                "PubMed Papers",
                stats.get("pubmed", 0)
            )

            st.metric(
                "Knowledge Graph Facts",
                stats.get("graph", 0)
            )

            st.metric(
                "Response Time",
                f"{stats.get('time',0):.2f} sec"
            )

        st.markdown("---")

        # ======================================
        # Backend Information
        # ======================================

        st.subheader("⚙ Backend")

        st.success("LLM : Llama 3.3 70B")

        st.success("Embeddings : BGE Large")

        st.success("Reranker : BGE Reranker")

        st.success("Vector DB : Qdrant")

        st.success("Knowledge Graph : Neo4j")

        st.success("Medical NER : SciSpaCy")

        st.success("Research : PubMed")

        st.markdown("---")

        # ======================================
        # About
        # ======================================

        st.subheader("ℹ About")

        st.write(
            """
This Oncology Agentic RAG system combines

- Hybrid Retrieval
- PubMed Search
- Knowledge Graph
- Semantic Search
- CrossEncoder Reranking
- Large Language Models

to generate evidence-based oncology answers.
"""
        )

    return {
        "pdf": pdf_enabled,
        "pubmed": pubmed_enabled,
        "graph": graph_enabled
    }