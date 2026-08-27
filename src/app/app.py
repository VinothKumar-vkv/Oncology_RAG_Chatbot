import time
import streamlit as st
from src.app.sidebar import render_sidebar
from src.llm.rag_pipeline import OncologyRAG

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Oncology Agentic RAG",
    page_icon="🩺",
    layout="wide"
)

# ==========================================================
# Session State
# ==========================================================

if "rag" not in st.session_state:
    st.session_state.rag = OncologyRAG()

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================================
# Header
# ==========================================================

st.title("🩺 Oncology Agentic RAG")

st.markdown(
"""
Hybrid Medical Retrieval using

- 📚 Medical Textbook
- 🧬 PubMed
- 🕸 Knowledge Graph
- 🤖 Llama 3.3 70B
"""
)

st.divider()

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header("⚙ Retrieval")

    use_pdf = st.checkbox(
        "Medical Textbook",
        value=True
    )

    use_pubmed = st.checkbox(
        "PubMed",
        value=True
    )

    use_graph = st.checkbox(
        "Knowledge Graph",
        value=True
    )

    st.divider()

    st.header("ℹ Statistics")

    chunk_placeholder = st.empty()

    pubmed_placeholder = st.empty()

    graph_placeholder = st.empty()

    time_placeholder = st.empty()

# ==========================================================
# Question
# ==========================================================

question = st.text_input(

    "Ask an Oncology Question",

    placeholder="Example: What is HER2 positive breast cancer?"

)

ask = st.button(

    "Ask",

    type="primary",

    use_container_width=True

)

# ==========================================================
# Ask Question
# ==========================================================

if ask:

    if question.strip() == "":

        st.warning("Please enter a question.")

        st.stop()

    with st.spinner("Retrieving evidence..."):

        start = time.time()

        result = st.session_state.rag.ask(question)

        end = time.time()

# ----------------------------------------------------------

    if isinstance(result, dict):

        answer = result.get("answer", "")

        pdf_docs = result.get("pdf_docs", [])

        pubmed_docs = result.get("pubmed_docs", [])

        kg_docs = result.get("kg_docs", [])

    else:

        answer = result

        pdf_docs = []

        pubmed_docs = []

        kg_docs = []

# ----------------------------------------------------------

    chunk_placeholder.metric(

        "PDF Chunks",

        len(pdf_docs)

    )

    pubmed_placeholder.metric(

        "PubMed Papers",

        len(pubmed_docs)

    )

    graph_placeholder.metric(

        "Graph Facts",

        len(kg_docs)

    )

    time_placeholder.metric(

        "Response Time",

        f"{end-start:.2f}s"

    )

# ----------------------------------------------------------

    st.session_state.history.append(

        {

            "question": question,

            "answer": answer

        }

    )

# ==========================================================
# Tabs
# ==========================================================

    tab1, tab2, tab3, tab4 = st.tabs(

        [

            "💬 Answer",

            "📄 Evidence",

            "🕸 Knowledge Graph",

            "🐞 Debug"

        ]

    )

# ==========================================================
# Answer
# ==========================================================

    with tab1:

        st.markdown(answer)

# ==========================================================
# Evidence
# ==========================================================

    with tab2:

        st.subheader("Medical Textbook")

        if len(pdf_docs) == 0:

            st.info("No textbook evidence.")

        else:

            for doc in pdf_docs:

                with st.expander(

                    f"Page {doc['page']}"

                ):

                    st.write(doc["text"])

# ----------------------------------------------------------

        st.subheader("PubMed")

        if len(pubmed_docs) == 0:

            st.info("No PubMed evidence.")

        else:

          for doc in pubmed_docs:

            with st.expander(doc.get("title","PubMed")):

                st.write(doc.get("abstract",""))

# ==========================================================
# Graph
# ==========================================================

    from src.app.graph_view import GraphViewer

    with tab3:

        st.subheader("🕸 Knowledge Graph")

        if len(kg_docs) == 0:

            st.info("No graph facts found.")

        else:

            viewer = GraphViewer()

            viewer.draw(kg_docs)
# ==========================================================
# Debug
# ==========================================================

    with tab4:

        st.write(result)

# ==========================================================
# History
# ==========================================================

if len(st.session_state.history):

    st.divider()

    st.subheader("Conversation History")

    for item in reversed(

        st.session_state.history

    ):

        with st.expander(

            item["question"]

        ):

            st.write(item["answer"])

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(

    "Built using Hybrid RAG • PubMed • Neo4j • Llama 3.3"

)