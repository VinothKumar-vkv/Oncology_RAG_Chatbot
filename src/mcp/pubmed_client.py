import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class PubMedMCPClient:

    def __init__(self):

        self.server = StdioServerParameters(
            command="python",
            args=["-m", "src.mcp.pubmed_server"]
        )

    async def search(self, query, max_results=5):

        async with stdio_client(self.server) as (read_stream, write_stream):

            async with ClientSession(
                read_stream,
                write_stream
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    "pubmed_search",
                    {
                        "query": query,
                        "max_results": max_results
                    }
                )

                return result