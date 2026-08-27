import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import json
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

from src.chatbot import OncologyChatbot


print("=" * 80)
print("Loading Oncology Chatbot...")
print("=" * 80)

chatbot = OncologyChatbot()

questions = []
answers = []
contexts = []
ground_truths = []

# Load evaluation dataset
with open("metrics_evaluation/evaluation_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"\nLoaded {len(data)} evaluation questions.\n")

for sample in data:

    print("=" * 80)
    print("Question:", sample["question"])
    print("=" * 80)

    result = chatbot.ask(sample["question"])

    questions.append(sample["question"])
    answers.append(result["answer"])
    contexts.append(result["contexts"])
    ground_truths.append(sample["ground_truth"])

print("\nCreating RAGAS Dataset...")

dataset = Dataset.from_dict(
    {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }
)

print("Running RAGAS Evaluation...\n")

results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
)

print("\n")
print("=" * 80)
print("RAGAS RESULTS")
print("=" * 80)

print(results)