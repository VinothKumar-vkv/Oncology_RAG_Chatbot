from Bio import Entrez
from typing import List, Dict


class PubMedRetriever:
    """
    Retrieves oncology-related articles from PubMed.
    """

    def __init__(self, email: str):
        """
        Initialize PubMed connection.

        Args:
            email (str): Your email address required by NCBI.
        """
        Entrez.email = email

    def search(self, query: str, max_results: int = 5):
            """
            Search PubMed and return PMIDs.

            Args:
                query (str): Search query.
                max_results (int): Number of articles.

            Returns:
                List[str]: PubMed IDs
            """

            try:
                handle = Entrez.esearch(
                    db="pubmed",
                    term=query,
                    retmax=max_results,
                    sort="relevance"
                )

                results = Entrez.read(handle)
                handle.close()

                return results["IdList"]

            except Exception as e:
                print(f"PubMed Search Error: {e}")
                return []

    def fetch_details(self, pmids: List[str]):
            """
            Fetch article information using PMIDs.

            Args:
                pmids (List[str]): List of PubMed IDs

            Returns:
                List[Dict]: Article details
            """

            if not pmids:
                return []

            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    id=",".join(pmids),
                    rettype="abstract",
                    retmode="xml"
                )

                records = Entrez.read(handle)
                handle.close()

                articles = []

                for article in records["PubmedArticle"]:

                    citation = article["MedlineCitation"]
                    article_data = citation["Article"]

                    title = article_data.get("ArticleTitle", "")

                    abstract = ""
                    if "Abstract" in article_data:
                        abstract = " ".join(article_data["Abstract"]["AbstractText"])

                    journal = article_data["Journal"]["Title"]

                    year = "Unknown"
                    try:
                        year = article_data["Journal"]["JournalIssue"]["PubDate"]["Year"]
                    except Exception:
                        pass

                    articles.append({
                        "title": title,
                        "abstract": abstract,
                        "journal": journal,
                        "year": year
                    })

                return articles

            except Exception as e:
                print(f"PubMed Fetch Error: {e}")
                return []

    def retrieve(self, query: str, max_results: int = 5):
            """
            Complete PubMed retrieval pipeline.

            Args:
                query (str): User query
                max_results (int): Number of articles to retrieve

            Returns:
                List[Dict]: Retrieved PubMed articles
            """

            pmids = self.search(query, max_results)

            if not pmids:
                return []

            articles = self.fetch_details(pmids)

            return articles