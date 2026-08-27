import json
from pathlib import Path

import pandas as pd

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score

from rouge_score import rouge_scorer

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = BASE_DIR / "results.csv"

OUTPUT_CSV = BASE_DIR / "results.csv"

OUTPUT_EXCEL = BASE_DIR / "results.xlsx"

# ==========================================================
# Load Results
# ==========================================================

print("=" * 80)
print("Loading Evaluation Results...")
print("=" * 80)

results = pd.read_csv(RESULTS_FILE)

print(f"\nLoaded {len(results)} evaluation samples.\n")

# ==========================================================
# Initialize Metrics
# ==========================================================

smooth = SmoothingFunction().method1

rouge = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True
)

# ==========================================================
# Create Metric Columns
# ==========================================================

results["BLEU"] = 0.0

results["ROUGE-1"] = 0.0

results["ROUGE-2"] = 0.0

results["ROUGE-L"] = 0.0

results["METEOR"] = 0.0

# ==========================================================
# Compute BLEU / ROUGE / METEOR
# ==========================================================

print("=" * 80)
print("Computing BLEU, ROUGE and METEOR...")
print("=" * 80)

for index, row in results.iterrows():

    reference = str(row["ground_truth"])

    prediction = str(row["generated_answer"])

    # ------------------------------------------------------
    # BLEU
    # ------------------------------------------------------

    bleu = sentence_bleu(
        [reference.split()],
        prediction.split(),
        smoothing_function=smooth
    )

    results.loc[index, "BLEU"] = round(bleu, 4)

    # ------------------------------------------------------
    # ROUGE
    # ------------------------------------------------------

    scores = rouge.score(reference, prediction)

    results.loc[index, "ROUGE-1"] = round(
        scores["rouge1"].fmeasure,
        4
    )

    results.loc[index, "ROUGE-2"] = round(
        scores["rouge2"].fmeasure,
        4
    )

    results.loc[index, "ROUGE-L"] = round(
        scores["rougeL"].fmeasure,
        4
    )

    # ------------------------------------------------------
    # METEOR
    # ------------------------------------------------------

    meteor = meteor_score(
        [reference.split()],
        prediction.split()
    )

    results.loc[index, "METEOR"] = round(
        meteor,
        4
    )

print("\nCompleted:")
print("✔ BLEU")
print("✔ ROUGE-1")
print("✔ ROUGE-2")
print("✔ ROUGE-L")
print("✔ METEOR")
print()
# ==========================================================
# BERTScore
# ==========================================================

from bert_score import score

print("=" * 80)
print("Computing BERTScore...")
print("=" * 80)

# Create column
results["BERTScore"] = 0.0

predictions = results["generated_answer"].fillna("").astype(str).tolist()
references = results["ground_truth"].fillna("").astype(str).tolist()

print("Calculating semantic similarity...")

try:
    # Precision, Recall and F1
    P, R, F1 = score(
        predictions,
        references,
        lang="en",
        verbose=True
    )

    results["BERTScore"] = [
        round(float(x), 4)
        for x in F1
    ]

    print("\n✔ BERTScore Completed")

except Exception as e:
    print("\nError while computing BERTScore")
    print(e)

print()

# ==========================================================
# Average Scores
# ==========================================================

print("=" * 80)
print("Average Evaluation Scores")
print("=" * 80)

print(f"BLEU        : {results['BLEU'].mean():.4f}")
print(f"ROUGE-1     : {results['ROUGE-1'].mean():.4f}")
print(f"ROUGE-2     : {results['ROUGE-2'].mean():.4f}")
print(f"ROUGE-L     : {results['ROUGE-L'].mean():.4f}")
print(f"METEOR      : {results['METEOR'].mean():.4f}")
print(f"BERTScore   : {results['BERTScore'].mean():.4f}")

print()

# ==========================================================
# Save Results
# ==========================================================

results.to_csv(
    OUTPUT_CSV,
    index=False
)

results.to_excel(
    OUTPUT_EXCEL,
    index=False
)

print("=" * 80)
print("Evaluation Completed Successfully")
print("=" * 80)

print(f"\nCSV Saved To:\n{OUTPUT_CSV}")

print(f"\nExcel Saved To:\n{OUTPUT_EXCEL}")

print()