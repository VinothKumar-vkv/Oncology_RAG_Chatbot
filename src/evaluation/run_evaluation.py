import json
import csv
from pathlib import Path

from src.chatbot import OncologyChatbot
from src.evaluation.llm_judge import LLMJudge

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

QUESTIONS_FILE = BASE_DIR / "questions.json"
RESULTS_FILE = BASE_DIR / "results.csv"

# ==========================================================
# Initialize Chatbot
# ==========================================================

print("\nInitializing Oncology Agentic RAG...")

chatbot = OncologyChatbot()
judge = LLMJudge()

# ==========================================================
# Load Evaluation Questions
# ==========================================================

with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"\nLoaded {len(questions)} evaluation questions.\n")

results = []

# ==========================================================
# Run Evaluation
# ==========================================================

for item in questions:

    print("=" * 90)
    print(f"Question {item['id']}: {item['question']}")
    print("=" * 90)

    output = chatbot.ask(item["question"])

    # ------------------------------------------------------
    # Retrieved Context
    # ------------------------------------------------------

    retrieved_context = ""

    if "documents" in output:

        retrieved_context = "\n\n".join(
            [
                getattr(doc, "page_content", str(doc))
                for doc in output["documents"]
            ]
        )

    # ------------------------------------------------------
    # Number of Retrieved Documents
    # ------------------------------------------------------

    retrieved_docs = len(output.get("documents", []))
    # ------------------------------------------------------
    # LLM-as-a-Judge Evaluation
    # ------------------------------------------------------

    scores = judge.evaluate(
        question=item["question"],
        context=retrieved_context,
        generated_answer=output["answer"],
        reference_answer=item.get("reference_answer", "")
    )

    # ------------------------------------------------------
    # Store Results
    # ------------------------------------------------------

    results.append({

    "id": item["id"],

    "question": item["question"],

    "ground_truth": item.get("reference_answer", ""),

    "generated_answer": output["answer"],

    "retrieved_context": retrieved_context,

    "retrieved_documents": retrieved_docs,

    "Faithfulness (%)": scores["Faithfulness (%)"],

    "Answer Relevancy (%)": scores["Answer Relevancy (%)"],

    "Context Precision (%)": scores["Context Precision (%)"],

    "Context Recall (%)": scores["Context Recall (%)"],

    "retrieval_time": round(output["retrieval_time"], 3),

    "reranking_time": round(output["reranking_time"], 3),

    "generation_time": round(output["generation_time"], 3),

    "total_time": round(output["total_time"], 3)

})

# ==========================================================
# Save Results
# ==========================================================

fieldnames = [

    "id",

    "question",

    "ground_truth",

    "generated_answer",

    "retrieved_context",

    "retrieved_documents",

    "Faithfulness (%)",

    "Answer Relevancy (%)",

    "Context Precision (%)",

    "Context Recall (%)",

    "retrieval_time",

    "reranking_time",

    "generation_time",

    "total_time"

]

with open(
    RESULTS_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(results)

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 90)
print("Evaluation Completed Successfully!")
print("=" * 90)

print(f"\nQuestions Evaluated : {len(results)}")

avg_retrieval = sum(r["retrieval_time"] for r in results) / len(results)
avg_rerank = sum(r["reranking_time"] for r in results) / len(results)
avg_generation = sum(r["generation_time"] for r in results) / len(results)
avg_total = sum(r["total_time"] for r in results) / len(results)

print(f"Average Retrieval Time : {avg_retrieval:.3f} sec")
print(f"Average Reranking Time : {avg_rerank:.3f} sec")
print(f"Average Generation Time: {avg_generation:.3f} sec")
print(f"Average Total Time     : {avg_total:.3f} sec")

avg_faithfulness = sum(r["Faithfulness (%)"] for r in results) / len(results)
avg_answer = sum(r["Answer Relevancy (%)"] for r in results) / len(results)
avg_precision = sum(r["Context Precision (%)"] for r in results) / len(results)
avg_recall = sum(r["Context Recall (%)"] for r in results) / len(results)

print("\nLLM-as-a-Judge Evaluation")
print("-" * 40)
print(f"Average Faithfulness      : {avg_faithfulness:.2f}%")
print(f"Average Answer Relevancy  : {avg_answer:.2f}%")
print(f"Average Context Precision : {avg_precision:.2f}%")
print(f"Average Context Recall    : {avg_recall:.2f}%")

print(f"\nResults saved to:\n{RESULTS_FILE}")