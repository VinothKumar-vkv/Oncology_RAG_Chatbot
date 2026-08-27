import time
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util


class RAGEvaluator:

    def __init__(self):

        self.embedder = SentenceTransformer(
            "BAAI/bge-large-en-v1.5"
        )

        self.rouge = rouge_scorer.RougeScorer(
            ["rouge1", "rougeL"],
            use_stemmer=True
        )

    # ---------------------------------------------
    # Semantic Similarity
    # ---------------------------------------------

    def semantic_similarity(self, answer, reference):

        emb1 = self.embedder.encode(
            answer,
            convert_to_tensor=True
        )

        emb2 = self.embedder.encode(
            reference,
            convert_to_tensor=True
        )

        score = util.cos_sim(emb1, emb2)

        return float(score)

    # ---------------------------------------------
    # ROUGE
    # ---------------------------------------------

    def rouge_score(self, answer, reference):

        scores = self.rouge.score(
            reference,
            answer
        )

        return {

            "ROUGE-1":
                round(scores["rouge1"].fmeasure, 3),

            "ROUGE-L":
                round(scores["rougeL"].fmeasure, 3)
        }

    # ---------------------------------------------
    # Context Precision
    # ---------------------------------------------

    def context_precision(self, retrieved_docs, answer):

        if len(retrieved_docs) == 0:
            return 0

        relevant = 0

        for doc in retrieved_docs:

            if doc["text"][:100].lower() in answer.lower():

                relevant += 1

        return round(

            relevant / len(retrieved_docs),

            3

        )

    # ---------------------------------------------
    # Context Recall
    # ---------------------------------------------

    def context_recall(self, retrieved_docs, answer):

        if len(retrieved_docs) == 0:

            return 0

        matched = 0

        for doc in retrieved_docs:

            overlap = self.semantic_similarity(

                doc["text"][:500],

                answer

            )

            if overlap > 0.60:

                matched += 1

        return round(

            matched / len(retrieved_docs),

            3

        )

    # ---------------------------------------------
    # Faithfulness
    # ---------------------------------------------

    def faithfulness(self, retrieved_docs, answer):

        if len(retrieved_docs) == 0:

            return 0

        context = "\n".join(

            [

                d["text"]

                for d in retrieved_docs

            ]

        )

        return round(

            self.semantic_similarity(

                answer,

                context

            ),

            3

        )

    # ---------------------------------------------
    # Hallucination
    # ---------------------------------------------

    def hallucination_score(self, faithfulness):

        return round(

            1 - faithfulness,

            3

        )

    # ---------------------------------------------
    # Complete Evaluation
    # ---------------------------------------------

    def evaluate(

        self,

        retrieved_docs,

        answer,

        reference=None,

        latency=0

    ):

        metrics = {}

        metrics["Latency"] = round(

            latency,

            2

        )

        metrics["Faithfulness"] = self.faithfulness(

            retrieved_docs,

            answer

        )

        metrics["Context Precision"] = self.context_precision(

            retrieved_docs,

            answer

        )

        metrics["Context Recall"] = self.context_recall(

            retrieved_docs,

            answer

        )

        metrics["Hallucination"] = self.hallucination_score(

            metrics["Faithfulness"]

        )

        if reference:

            metrics.update(

                self.rouge_score(

                    answer,

                    reference

                )

            )

            metrics["Semantic Similarity"] = round(

                self.semantic_similarity(

                    answer,

                    reference

                ),

                3

            )

        return metrics