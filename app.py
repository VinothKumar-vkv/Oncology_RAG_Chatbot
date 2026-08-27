import streamlit as st
from src.chatbot import OncologyChatbot
import time

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Oncology Agentic RAG",
    page_icon="🩺",
    layout="wide"
)

# -------------------------------------------------
# Load Chatbot Once
# -------------------------------------------------

@st.cache_resource
def load_chatbot():
    return OncologyChatbot()

chatbot = load_chatbot()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:

    st.title("🩺 Oncology Agentic RAG")

    st.markdown("---")

    st.subheader("System")

    st.success("✅ Hybrid Retrieval")

    st.write("• Qdrant")

    st.write("• BM25")

    st.write("• Knowledge Graph")

    st.write("• PubMed")

    st.write("• CrossEncoder")

    st.write("• Qwen 2.5")

    st.markdown("---")

    st.subheader("Dataset")

    st.info("65,725 Oncology Chunks")

    st.markdown("---")

    st.caption("Developed using Agentic RAG")

# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🧬 Oncology Agentic RAG")

st.write(
    "Ask any oncology-related medical question. "
    "The answer is generated using Hybrid Retrieval "
    "(Qdrant + BM25 + Knowledge Graph + PubMed)."
)

st.divider()

# -------------------------------------------------
# Input
# -------------------------------------------------

query = st.text_input(
    "Ask an Oncology Question",
    placeholder="Example: What is HER2 positive breast cancer?"
)

col1, col2 = st.columns([1,1])

ask = col1.button("🔍 Generate Answer")

clear = col2.button("🗑 Clear")

if clear:
    st.rerun()

# -------------------------------------------------
# Run Chatbot
# -------------------------------------------------

if ask and query:

    with st.spinner("Generating answer..."):

        start = time.time()

        print("\n========== APP BEFORE CHATBOT ==========")

        result = chatbot.ask(query)

        print("\n========== APP AFTER CHATBOT ==========")

        end = time.time()

    # -------------------------------------------------
    # Answer
    # -------------------------------------------------

    st.success("Answer Generated")

    st.subheader("🤖 Answer")

    st.write(result["answer"])

    # -------------------------------------------------
    # References
    # -------------------------------------------------

    st.subheader("📚 Retrieved Evidence")

    for i, doc in enumerate(result["documents"], start=1):

        with st.expander(
            f"{i}. {doc['source']} | {doc.get('filename','')}"
        ):

            st.write(doc["text"])

            if "rerank_score" in doc:

                st.metric(
                    "Rerank Score",
                    f"{doc['rerank_score']:.4f}"
                )

            if "score" in doc:

                st.metric(
                    "Retrieval Score",
                    f"{doc['score']:.4f}"
                )

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    st.subheader("⚡ Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Retrieval",
        f"{result['retrieval_time']:.2f}s"
    )

    c2.metric(
        "Reranking",
        f"{result['reranking_time']:.2f}s"
    )

    c3.metric(
        "Generation",
        f"{result['generation_time']:.2f}s"
    )

    c4.metric(
        "Total",
        f"{result['total_time']:.2f}s"
    )

    st.caption(f"Execution Time: {end-start:.2f} sec")