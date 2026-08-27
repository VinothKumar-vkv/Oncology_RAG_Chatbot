from src.retrieval.search import OncologySearcher

searcher = OncologySearcher()

results = searcher.search("What is breast cancer?", top_k=5)

for i, doc in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}")
    print(f"Score    : {doc['score']:.4f}")
    print(f"File     : {doc['filename']}")
    print(f"Page     : {doc['page']}")
    print(f"Chunk ID : {doc['chunk_id']}")
    print(doc["text"][:500])
    print()