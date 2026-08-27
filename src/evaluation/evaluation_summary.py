import pandas as pd
from pathlib import Path

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = BASE_DIR / "results.csv"

# ==========================================================
# Load Results
# ==========================================================

df = pd.read_csv(RESULTS_FILE)

print("=" * 80)
print("ONCOLOGY AGENTIC RAG - EVALUATION SUMMARY")
print("=" * 80)

# ==========================================================
# Number of Questions
# ==========================================================

print(f"\nQuestions Evaluated : {len(df)}")

# ==========================================================
# LLM-as-a-Judge Metrics
# ==========================================================

print("\nLLM-as-a-Judge Metrics")
print("-" * 40)

judge_metrics = [

    "Faithfulness (%)",

    "Answer Relevancy (%)",

    "Context Precision (%)",

    "Context Recall (%)"

]

for metric in judge_metrics:

    if metric in df.columns:

        print(f"{metric:<30}: {df[metric].mean():.2f}%")

# ==========================================================
# Performance Metrics
# ==========================================================

print("\nPerformance Metrics")
print("-" * 40)

performance_metrics = [

    "retrieval_time",

    "reranking_time",

    "generation_time",

    "total_time"

]

for metric in performance_metrics:

    if metric in df.columns:

        print(f"{metric:<30}: {df[metric].mean():.3f} sec")

# ==========================================================
# Retrieval Statistics
# ==========================================================

if "retrieved_documents" in df.columns:

    print("\nRetrieval Statistics")
    print("-" * 40)

    print(
        f"Average Retrieved Documents : "
        f"{df['retrieved_documents'].mean():.2f}"
    )

# ==========================================================
# Save Summary
# ==========================================================

summary_file = BASE_DIR / "evaluation_summary.txt"

with open(summary_file, "w") as f:

    f.write("=" * 80 + "\n")
    f.write("ONCOLOGY AGENTIC RAG - EVALUATION SUMMARY\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"Questions Evaluated : {len(df)}\n\n")

    f.write("LLM-as-a-Judge Metrics\n")
    f.write("-" * 40 + "\n")

    for metric in judge_metrics:

        if metric in df.columns:

            f.write(
                f"{metric:<30}: "
                f"{df[metric].mean():.2f}%\n"
            )

    f.write("\nPerformance Metrics\n")
    f.write("-" * 40 + "\n")

    for metric in performance_metrics:

        if metric in df.columns:

            f.write(
                f"{metric:<30}: "
                f"{df[metric].mean():.3f} sec\n"
            )

    if "retrieved_documents" in df.columns:

        f.write("\nRetrieval Statistics\n")
        f.write("-" * 40 + "\n")

        f.write(
            f"Average Retrieved Documents : "
            f"{df['retrieved_documents'].mean():.2f}\n"
        )

print("\nSummary saved to:")
print(summary_file)