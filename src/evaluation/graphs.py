import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = BASE_DIR / "results.csv"

FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# =====================================================
# Load Results
# =====================================================

df = pd.read_csv(RESULTS_FILE)

# =====================================================
# Graph 1: Average Processing Time
# =====================================================

times = [
    df["retrieval_time"].mean(),
    df["reranking_time"].mean(),
    df["generation_time"].mean(),
    df["total_time"].mean()
]

labels = [
    "Retrieval",
    "Reranking",
    "Generation",
    "Total"
]

plt.figure(figsize=(8, 5))
plt.bar(labels, times)

plt.title("Average Processing Time")
plt.xlabel("Pipeline Stage")
plt.ylabel("Time (seconds)")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "average_processing_time.png",
    dpi=300
)

plt.close()

print("✓ Saved: average_processing_time.png")

# =====================================================
# Graph 2: Average Answer Quality Metrics
# =====================================================

metrics = [
    df["BLEU"].mean(),
    df["ROUGE-1"].mean(),
    df["ROUGE-2"].mean(),
    df["ROUGE-L"].mean(),
    df["METEOR"].mean(),
    df["BERTScore"].mean()
]

metric_names = [
    "BLEU",
    "ROUGE-1",
    "ROUGE-2",
    "ROUGE-L",
    "METEOR",
    "BERTScore"
]

plt.figure(figsize=(9, 5))

plt.bar(metric_names, metrics)

plt.title("Average Evaluation Metrics")
plt.xlabel("Metric")
plt.ylabel("Score")

plt.ylim(0, 1)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "average_evaluation_metrics.png",
    dpi=300
)

plt.close()

print("✓ Saved: average_evaluation_metrics.png")

# =====================================================
# Graph 3: Processing Time per Question
# =====================================================

plt.figure(figsize=(10,6))

plt.plot(df["id"], df["retrieval_time"],
         marker='o',
         label="Retrieval")

plt.plot(df["id"], df["reranking_time"],
         marker='s',
         label="Reranking")

plt.plot(df["id"], df["generation_time"],
         marker='^',
         label="Generation")

plt.xlabel("Question ID")
plt.ylabel("Time (seconds)")
plt.title("Processing Time for Each Evaluation Question")

plt.xticks(df["id"])

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "processing_time_per_question.png",
    dpi=300
)

plt.close()

print("✓ Saved: processing_time_per_question.png")

# =====================================================
# Graph 4: Quality Metrics per Question
# =====================================================

plt.figure(figsize=(12,6))

plt.plot(df["id"], df["BLEU"], marker='o', label="BLEU")
plt.plot(df["id"], df["ROUGE-L"], marker='s', label="ROUGE-L")
plt.plot(df["id"], df["METEOR"], marker='^', label="METEOR")
plt.plot(df["id"], df["BERTScore"], marker='d', label="BERTScore")

plt.xlabel("Question ID")
plt.ylabel("Score")
plt.title("Evaluation Metrics Across Oncology Questions")

plt.xticks(df["id"])
plt.ylim(0,1)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "quality_metrics_per_question.png",
    dpi=300
)

plt.close()

print("✓ Saved: quality_metrics_per_question.png")

# =====================================================
# Graph 5: Latency Breakdown
# =====================================================

avg_times = [
    df["retrieval_time"].mean(),
    df["reranking_time"].mean(),
    df["generation_time"].mean()
]

labels = [
    "Retrieval",
    "Reranking",
    "Generation"
]

plt.figure(figsize=(7,7))

plt.pie(
    avg_times,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Average Latency Distribution")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "latency_distribution.png",
    dpi=300
)

plt.close()

print("✓ Saved: latency_distribution.png")