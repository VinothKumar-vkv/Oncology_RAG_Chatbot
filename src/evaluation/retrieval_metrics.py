"""
retrieval_metrics.py

Evaluation metrics for Hybrid Retrieval in Oncology Agentic RAG.
"""

from collections import Counter, defaultdict


# ============================================================
# Source Contribution
# ============================================================

def source_contribution(retrieved_docs):
    """
    Percentage contribution of each retrieval source.
    """

    total = len(retrieved_docs)

    if total == 0:
        return {}

    counts = Counter(doc["source"] for doc in retrieved_docs)

    return {
        source: round((count / total) * 100, 2)
        for source, count in counts.items()
    }


# ============================================================
# Source Counts
# ============================================================

def source_counts(retrieved_docs):

    return dict(Counter(doc["source"] for doc in retrieved_docs))


# ============================================================
# Average Search Score by Source
# ============================================================

def average_search_score(retrieved_docs):

    scores = defaultdict(list)

    for doc in retrieved_docs:

        if "score" in doc:

            scores[doc["source"]].append(float(doc["score"]))

    return {

        source: round(sum(values) / len(values), 4)

        for source, values in scores.items()

        if len(values) > 0

    }


# ============================================================
# Average Rerank Score by Source
# ============================================================

def average_rerank_score(retrieved_docs):

    scores = defaultdict(list)

    for doc in retrieved_docs:

        if "rerank_score" in doc:

            scores[doc["source"]].append(float(doc["rerank_score"]))

    return {

        source: round(sum(values) / len(values), 4)

        for source, values in scores.items()

        if len(values) > 0

    }


# ============================================================
# Hit Rate@K
# ============================================================

def hit_rate_at_k(retrieved_docs, relevant_chunk_ids):

    if not relevant_chunk_ids:
        return 0

    for doc in retrieved_docs:

        if doc["chunk_id"] in relevant_chunk_ids:
            return 1

    return 0


# ============================================================
# Precision@K
# ============================================================

def precision_at_k(retrieved_docs, relevant_chunk_ids):

    if len(retrieved_docs) == 0:
        return 0

    if not relevant_chunk_ids:
        return 0

    relevant = sum(

        1

        for doc in retrieved_docs

        if doc["chunk_id"] in relevant_chunk_ids

    )

    return round(relevant / len(retrieved_docs), 4)


# ============================================================
# Recall@K
# ============================================================

def recall_at_k(retrieved_docs, relevant_chunk_ids):

    if not relevant_chunk_ids:
        return 0

    relevant = sum(

        1

        for doc in retrieved_docs

        if doc["chunk_id"] in relevant_chunk_ids

    )

    return round(relevant / len(relevant_chunk_ids), 4)


# ============================================================
# Reciprocal Rank
# ============================================================

def reciprocal_rank(retrieved_docs, relevant_chunk_ids):

    if not relevant_chunk_ids:
        return 0

    for rank, doc in enumerate(retrieved_docs, start=1):

        if doc["chunk_id"] in relevant_chunk_ids:
            return round(1 / rank, 4)

    return 0


# ============================================================
# Mean Reciprocal Rank
# ============================================================

def mean_reciprocal_rank(list_of_queries):

    """
    list_of_queries =
    [
        {
            "retrieved_docs": [...],
            "relevant_chunk_ids": [...]
        },
        ...
    ]
    """

    if len(list_of_queries) == 0:
        return 0

    total = 0

    for item in list_of_queries:

        total += reciprocal_rank(
            item["retrieved_docs"],
            item["relevant_chunk_ids"]
        )

    return round(total / len(list_of_queries), 4)


# ============================================================
# Retrieval Summary
# ============================================================

def retrieval_summary(retrieved_docs):

    summary = {}

    summary["total_documents"] = len(retrieved_docs)

    summary["source_counts"] = source_counts(retrieved_docs)

    summary["source_contribution"] = source_contribution(retrieved_docs)

    summary["average_search_score"] = average_search_score(retrieved_docs)

    summary["average_rerank_score"] = average_rerank_score(retrieved_docs)

    return summary


# ============================================================
# Example
# ============================================================

if __name__ == "__main__":

    docs = [

        {
            "source": "Qdrant",
            "chunk_id": "100",
            "score": 0.82,
            "rerank_score": 0.96
        },

        {
            "source": "BM25",
            "chunk_id": "200",
            "score": 12.4,
            "rerank_score": 0.73
        },

        {
            "source": "PubMed",
            "chunk_id": "-",
            "score": 0.0,
            "rerank_score": 0.41
        }

    ]

    relevant = {"100"}

    print("\nRetrieval Summary")
    print(retrieval_summary(docs))

    print("\nHit Rate")
    print(hit_rate_at_k(docs, relevant))

    print("\nPrecision@K")
    print(precision_at_k(docs, relevant))

    print("\nRecall@K")
    print(recall_at_k(docs, relevant))

    print("\nReciprocal Rank")
    print(reciprocal_rank(docs, relevant))