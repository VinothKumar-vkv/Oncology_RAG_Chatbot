from src.mcp.pubmed_tool import search_pubmed

results = search_pubmed(
    "HER2 positive breast cancer"
)

for paper in results:

    print("=" * 60)

    print("PMID :", paper["pmid"])

    print("Title :", paper["title"])

    print()

    print(paper["abstract"][:500])