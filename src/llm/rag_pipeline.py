from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import OncologyReranker
from src.retrieval.query_analyzer import MedicalQueryAnalyzer
from src.retrieval.context_fusion import ContextFusion
from src.evaluation.evaluator import RAGEvaluator
import time

from src.pubmed.pubmed_retriever import PubMedRetriever

from src.knowledge_graph.entity_extractor import MedicalEntityExtractor
from src.knowledge_graph.semantic_graph_retriever import SemanticGraphRetriever
from src.knowledge_graph.graph_filter import GraphFilter

from src.llm.prompt_builder import PromptBuilder
from src.llm.llama_client import LlamaClient


class OncologyRAG:

    def __init__(self):

        # -------------------------
        # Retrieval
        # -------------------------
        self.retriever = HybridRetriever()

        # -------------------------
        # PubMed
        # -------------------------
        self.pubmed = PubMedRetriever()

        # -------------------------
        # Knowledge Graph
        # -------------------------
        self.entity_extractor = MedicalEntityExtractor()
        self.graph_retriever = SemanticGraphRetriever()

        self.graph_filter = GraphFilter()

        # -------------------------
        # Merge Context
        # -------------------------
        self.fusion = ContextFusion()

        # -------------------------
        # Reranker
        # -------------------------
        self.reranker = OncologyReranker()

        # -------------------------
        # Query Analyzer
        # -------------------------
        self.analyzer = MedicalQueryAnalyzer()

        # -------------------------
        # LLM
        # -------------------------
        self.llm = LlamaClient()

        self.evaluator = RAGEvaluator()

    # ==========================================================
    # Retrieve Graph Context
    # ==========================================================

    def retrieve_graph(self, question, question_type):

            entities = self.entity_extractor.extract(question)

            print("\nDetected Entities:")
            print(entities)

            kg_docs = []

            for entity in entities:

                try:

                    # Semantic graph retrieval
                    results = self.graph_retriever.retrieve(entity)

                    kg_docs.extend(results)

                except Exception as e:

                    print(f"Graph retrieval failed for '{entity}'")

                    print(e)

            # Filter graph facts based on question type
            kg_docs = self.graph_filter.filter(
                kg_docs,
                question_type
            )

            return kg_docs

    # ==========================================================
    # Main Pipeline
    # ==========================================================

    def ask(self, question):

        print("\nAnalyzing Question...")

        question_type = self.analyzer.classify(question)

        print("Question Type :", question_type)

        pdf_docs = []
        pubmed_docs = []
        kg_docs = []

        # -------------------------------------------------
        # Definition
        # -------------------------------------------------

        if question_type == "definition":

            pdf_docs = self.retriever.search(question)

            kg_docs = self.retrieve_graph(
                question,
                question_type
            )

        # -------------------------------------------------
        # Symptoms
        # -------------------------------------------------

        elif question_type == "symptoms":

            pdf_docs = self.retriever.search(question)

        # -------------------------------------------------
        # Diagnosis
        # -------------------------------------------------

        elif question_type == "diagnosis":

            pdf_docs = self.retriever.search(question)

            kg_docs = self.retrieve_graph(
    question,
    question_type
)

        # -------------------------------------------------
        # Histopathology
        # -------------------------------------------------

        elif question_type == "histopathology":

            pdf_docs = self.retriever.search(question)

        # -------------------------------------------------
        # Treatment
        # -------------------------------------------------

        elif question_type == "treatment":

            pdf_docs = self.retriever.search(question)

            pubmed_docs = self.pubmed.search(question)

            kg_docs = self.retrieve_graph(
    question,
    question_type
)

        # -------------------------------------------------
        # Genetics
        # -------------------------------------------------

        elif question_type == "genetics":

            pdf_docs = self.retriever.search(question)

            kg_docs = self.retrieve_graph(
    question,
    question_type
)

        # -------------------------------------------------
        # Latest Research
        # -------------------------------------------------

        elif question_type == "latest_research":

            pubmed_docs = self.pubmed.search(question)

        # -------------------------------------------------
        # Clinical Case
        # -------------------------------------------------

        elif question_type == "clinical_case":

            pdf_docs = self.retriever.search(question)

            kg_docs = self.retrieve_graph(
    question,
    question_type
)

        # -------------------------------------------------
        # Prognosis
        # -------------------------------------------------

        elif question_type == "prognosis":

                pdf_docs = self.retriever.search(question)

                pubmed_docs = self.pubmed.search(
                    question + " prognosis review"
                )

        # -------------------------------------------------
        # Prevention
        # -------------------------------------------------

        elif question_type == "prevention":

            pdf_docs = self.retriever.search(question)

        # -------------------------------------------------
        # Default
        # -------------------------------------------------

        else:

            pdf_docs = self.retriever.search(question)

            pubmed_docs = self.pubmed.search(
    question + " clinical trial review"
)

            kg_docs = self.retrieve_graph(
    question,
    question_type
)

        # ==================================================
        # Merge Context
        # ==================================================

        merged_docs = self.fusion.merge(

            pdf_docs,

            pubmed_docs,

            kg_docs

        )
        print("\n========== Merged Documents ==========")

        for i, doc in enumerate(merged_docs):
            print(f"\nDocument {i+1}")
            print(type(doc))
            print(doc)

        # Remove duplicate contexts
        # --------------------------------------------------
        # Remove duplicate contexts safely
        # --------------------------------------------------

        # --------------------------------------------------
        # Remove duplicate contexts safely
        # --------------------------------------------------

        unique_docs = {}

        print("\n========== Checking Documents ==========")

        for i, doc in enumerate(merged_docs):

            print(f"\nDocument {i+1}")
            print(doc)

            if not isinstance(doc, dict):
                print("❌ Not a dictionary")
                continue

            if "text" not in doc:
                print("❌ Missing 'text' key")
                continue

            unique_docs[doc["text"]] = doc

        merged_docs = list(unique_docs.values())

        print("\nValid Documents :", len(merged_docs))

        # ==================================================
        # Rerank
        # ==================================================

        if len(merged_docs) == 0:

            return "No relevant evidence found."

        ranked_docs = self.reranker.rerank(
            question,
            merged_docs
        )

        docs = [

            doc

            for doc, score in ranked_docs

        ]

        # ==================================================
        # Prompt
        # ==================================================

        prompt = PromptBuilder.build(

            question,

            docs,

            question_type

        )

        # Uncomment while debugging
        # print(prompt)

        # ==================================================
        # LLM
        # ==================================================

        # ==================================================
        # LLM
        # ==================================================

        start = time.time()

        answer = self.llm.generate(prompt)

        latency = time.time() - start

        # ==================================================
        # Evaluation
        # ==================================================

        metrics = self.evaluator.evaluate(

            docs,

            answer,

            latency=latency

        )

        print("\n========== Evaluation ==========")

        for k, v in metrics.items():

            print(f"{k:25}: {v}")

        return {

            "answer": answer,

            "question_type": question_type,

            "pdf_docs": pdf_docs,

            "pubmed_docs": pubmed_docs,

            "kg_docs": kg_docs,

            "merged_docs": merged_docs,

            "metrics": metrics

        }

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    rag = OncologyRAG()

    while True:

        question = input("\nAsk Oncology Question (type 'exit' to quit): ")

        if question.lower() == "exit":

            break

        rag.graph_retriever.graph.close()

        answer = rag.ask(question)

        print("\n" + "=" * 80)

        print(answer)