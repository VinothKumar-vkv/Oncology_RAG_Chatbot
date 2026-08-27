from src.retrieval.pubmed_retriever import PubMedRetriever


def main():

    retriever = PubMedRetriever(
        email="vinothkumarvkv.in@gmail.com"   # Replace with your email
    )

    query = "Breast Cancer"

    results = retriever.retrieve(query)

    print("=" * 80)
    print(f"Retrieved {len(results)} articles")
    print("=" * 80)

    for i, article in enumerate(results, start=1):

        print(f"\nArticle {i}")
        print("-" * 80)
        print("Title   :", article["title"])
        print("Journal :", article["journal"])
        print("Year    :", article["year"])
        print("Abstract:")
        print(article["abstract"][:500], "...")
        print("-" * 80)


if __name__ == "__main__":
    main()