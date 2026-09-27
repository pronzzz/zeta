import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class RetailMCPClient:
    def __init__(self):
        server_script = os.path.join(os.path.dirname(__file__), "../../../mcp_servers/retail_inventory/server.py")
        self.server_params = StdioServerParameters(
            command="python3",
            args=[server_script]
        )

    def _run_sync(self, coro):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    async def _call_tool(self, name: str, args: dict):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments=args)
                return result.content

    def check_stock_level(self, sku: str, store: str) -> str:
        """Check the stock level for a given SKU at a specific store via MCP."""
        res = self._run_sync(self._call_tool("check_stock_level", {"sku": sku, "store": store}))
        # The result content is a list of TextContent objects
        return res[0].text if res else "No response"

    def flag_slow_movers(self, store: str, window_days: int, threshold: float) -> str:
        """Find SKUs in a store that are selling below a certain threshold via MCP."""
        res = self._run_sync(self._call_tool("flag_slow_movers", {"store": store, "window_days": window_days, "threshold": threshold}))
        return res[0].text if res else "No response"

    def draft_restock_suggestion(self, sku: str, store: str) -> str:
        """Draft a restock suggestion email for a specific SKU and store via MCP."""
        res = self._run_sync(self._call_tool("draft_restock_suggestion", {"sku": sku, "store": store}))
        return res[0].text if res else "No response"
