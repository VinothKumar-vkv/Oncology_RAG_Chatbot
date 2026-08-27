import sys
import os
import json

# Add project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.chatbot import OncologyChatbot

chatbot = OncologyChatbot()

with open(
    "metrics_evaluation/evaluation_dataset.json",
    "r",
    encoding="utf-8"
) as f:
    questions = json.load(f)

results = []

for sample in questions:

    print("=" * 80)
    print("Question :", sample["question"])
    print("=" * 80)

    output = chatbot.ask(sample["question"])

    results.append({

        "question": sample["question"],

        "ground_truth": sample["ground_truth"],

        "answer": output["answer"],

        "contexts": output["contexts"],

        "retrieval_time": output["retrieval_time"],

        "reranking_time": output["reranking_time"],

        "generation_time": output["generation_time"],

        "total_time": output["total_time"]

    })

print("\nSaving Results...")

with open(
    "metrics_evaluation/results_without_mcp.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nDone.")