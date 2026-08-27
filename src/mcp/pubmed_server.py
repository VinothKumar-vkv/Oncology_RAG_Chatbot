from fastmcp import FastMCP
from src.mcp.pubmed_tool import search_pubmed

# Create MCP Server
mcp = FastMCP("PubMed MCP Server")


@mcp.tool()
def pubmed_search(query: str, max_results: int = 5):
    """
    Search PubMed for biomedical literature.

    Args:
        query: Medical search query
        max_results: Number of papers to retrieve

    Returns:
        List of PubMed articles
    """
    return search_pubmed(query, max_results)


if __name__ == "__main__":
    mcp.run()