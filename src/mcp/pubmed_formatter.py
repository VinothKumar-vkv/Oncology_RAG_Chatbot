def format_pubmed_context(articles):

    context = []

    for article in articles:

        context.append(
            f"""
Title: {article['title']}
Journal: {article['journal']}
Year: {article['year']}
PMID: {article['pmid']}
DOI: {article['doi']}
Authors: {', '.join(article['authors'])}
Keywords: {', '.join(article['keywords'])}

Abstract:
{article['abstract']}
"""
        )

    return "\n\n------------------------\n\n".join(context)