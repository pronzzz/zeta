from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("RetailInventory")

@mcp.tool()
def check_stock_level(sku: str, store: str) -> str:
    """Check the stock level for a given SKU at a specific store."""
    return str(tools.check_stock_level(sku, store))

@mcp.tool()
def flag_slow_movers(store: str, window_days: int, threshold: float) -> str:
    """Find SKUs in a store that are selling below a certain threshold."""
    return str(tools.flag_slow_movers(store, window_days, threshold))

@mcp.tool()
def draft_restock_suggestion(sku: str, store: str) -> str:
    """Draft a restock suggestion email for a specific SKU and store."""
    return str(tools.draft_restock_suggestion(sku, store))

if __name__ == "__main__":
    # Ensure seed data is populated
    from seed_data import seed_data
    seed_data()
    mcp.run()
