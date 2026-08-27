from Bio import Entrez

# Replace with your email
Entrez.email = "your_email@example.com"


class PubMedRetriever:

    def search(self, query, max_results=5):

        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results
        )

        record = Entrez.read(handle)

        handle.close()

        ids = record["IdList"]

        if not ids:
            return []

        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="abstract",
            retmode="xml"
        )

        papers = Entrez.read(handle)

        handle.close()

        results = []

        for article in papers["PubmedArticle"]:

            article_data = article["MedlineCitation"]["Article"]

            title = article_data.get("ArticleTitle", "")

            abstract = ""

            if "Abstract" in article_data:
                abstract = " ".join(
                    str(x)
                    for x in article_data["Abstract"]["AbstractText"]
                )

            results.append({
                "title": title,
                "abstract": abstract
            })

        return results


if __name__ == "__main__":

    retriever = PubMedRetriever()

    papers = retriever.search(
        "HER2 breast cancer treatment"
    )

    for i, paper in enumerate(papers, start=1):

        print("=" * 80)
        print(f"Paper {i}")
        print()
        print(paper["title"])
        print()
        print(paper["abstract"][:800])