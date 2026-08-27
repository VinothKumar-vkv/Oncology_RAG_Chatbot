import json
import pandas as pd
import sacrebleu

from rouge_score import rouge_scorer
from nltk.translate.meteor_score import meteor_score
from bert_score import score as bertscore

# -----------------------------
# Load JSON files
# -----------------------------
with open("metrics_evaluation/results_with_mcp.json","r",encoding="utf-8") as f:
    with_mcp=json.load(f)

with open("metrics_evaluation/results_without_mcp.json","r",encoding="utf-8") as f:
    without_mcp=json.load(f)

# -----------------------------
# Metrics
# -----------------------------

rouge=rouge_scorer.RougeScorer(
    ['rouge1','rouge2','rougeL'],
    use_stemmer=True
)

rows=[]

for a,b in zip(with_mcp,without_mcp):

    gt=a["ground_truth"]

    ans1=a["answer"]
    ans2=b["answer"]

    bleu1=sacrebleu.sentence_bleu(ans1,[gt]).score
    bleu2=sacrebleu.sentence_bleu(ans2,[gt]).score

    r1=rouge.score(gt,ans1)
    r2=rouge.score(gt,ans2)

    meteor1=meteor_score([gt.split()],ans1.split())
    meteor2=meteor_score([gt.split()],ans2.split())

    P,R,F=bertscore(
        [ans1,ans2],
        [gt,gt],
        lang="en",
        verbose=False
    )

    rows.append({

        "Question":a["question"],

        "BLEU WITH":bleu1,
        "BLEU WITHOUT":bleu2,

        "ROUGE1 WITH":r1["rouge1"].fmeasure,
        "ROUGE1 WITHOUT":r2["rouge1"].fmeasure,

        "ROUGE2 WITH":r1["rouge2"].fmeasure,
        "ROUGE2 WITHOUT":r2["rouge2"].fmeasure,

        "ROUGEL WITH":r1["rougeL"].fmeasure,
        "ROUGEL WITHOUT":r2["rougeL"].fmeasure,

        "METEOR WITH":meteor1,
        "METEOR WITHOUT":meteor2,

        "BERTScore WITH":F[0].item(),
        "BERTScore WITHOUT":F[1].item(),

        "Retrieval WITH":a["retrieval_time"],
        "Retrieval WITHOUT":b["retrieval_time"],

        "Generation WITH":a["generation_time"],
        "Generation WITHOUT":b["generation_time"],

        "Total WITH":a["total_time"],
        "Total WITHOUT":b["total_time"]
    })

df=pd.DataFrame(rows)

print(df)

print("\n==========================")
print("AVERAGE METRICS")
print("==========================")

print(df.mean(numeric_only=True))

df.to_csv(
    "metrics_evaluation/final_metrics.csv",
    index=False
)

print("\nSaved final_metrics.csv")