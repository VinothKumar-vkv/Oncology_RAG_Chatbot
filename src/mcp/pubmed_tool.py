from Bio import Entrez

# Replace this with your email (required by NCBI)
Entrez.email = "your_email@gmail.com"


from Bio import Entrez

Entrez.email = "your_email@example.com"

from Bio import Entrez

Entrez.email = "your_email@example.com"


def search_pubmed(query, max_results=5):

    search = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results
    )

    ids = Entrez.read(search)["IdList"]

    if not ids:
        return []

    fetch = Entrez.efetch(
        db="pubmed",
        id=",".join(ids),
        rettype="abstract",
        retmode="xml"
    )

    records = Entrez.read(fetch)

    articles = []

    for record in records["PubmedArticle"]:

        citation = record["MedlineCitation"]
        article = citation["Article"]

        # PMID
        pmid = str(citation["PMID"])

        # Title
        title = str(article.get("ArticleTitle", ""))

        # Abstract
        abstract = ""
        if "Abstract" in article:
            abstract = " ".join(
                str(text)
                for text in article["Abstract"]["AbstractText"]
            )

        # Journal
        journal = article["Journal"]["Title"]

        # Publication Year
        year = "Unknown"

        pubdate = article["Journal"]["JournalIssue"]["PubDate"]

        if "Year" in pubdate:
            year = pubdate["Year"]
        elif "MedlineDate" in pubdate:
            year = pubdate["MedlineDate"]

        # Authors
        authors = []

        if "AuthorList" in article:

            for author in article["AuthorList"]:

                firstname = author.get("ForeName", "")
                lastname = author.get("LastName", "")

                name = f"{firstname} {lastname}".strip()

                if name:
                    authors.append(name)

        # DOI
        doi = ""

        if "PubmedData" in record:

            article_ids = record["PubmedData"]["ArticleIdList"]

            for article_id in article_ids:

                if article_id.attributes.get("IdType") == "doi":
                    doi = str(article_id)
                    break

        # MeSH Keywords
        keywords = []

        if "MeshHeadingList" in citation:

            for mesh in citation["MeshHeadingList"]:

                descriptor = mesh["DescriptorName"]

                keywords.append(str(descriptor))

        articles.append(
            {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "year": year,
                "journal": journal,
                "doi": doi,
                "authors": authors,
                "keywords": keywords
            }
        )

    return articles