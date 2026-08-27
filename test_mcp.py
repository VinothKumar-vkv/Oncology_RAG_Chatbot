import asyncio
from src.mcp.pubmed_client import PubMedMCPClient


async def main():

    client = PubMedMCPClient()

    result = await client.search(
        "HER2 positive breast cancer"
    )

    print(result)


asyncio.run(main())