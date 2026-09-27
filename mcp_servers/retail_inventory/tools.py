from db import get_connection

def check_stock_level(sku: str, store: str) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT on_hand_qty, reorder_point, sell_through_rate FROM inventory WHERE sku=? AND store=?", (sku, store))
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": "SKU or store not found"}
    
    qty, reorder, rate = row
    days_of_cover = round(qty / (rate * 10)) if rate > 0 else 999
    
    return {
        "sku": sku,
        "store": store,
        "on_hand_qty": qty,
        "reorder_point": reorder,
        "days_of_cover": days_of_cover,
        "sell_through_rate": rate
    }

def flag_slow_movers(store: str, window_days: int, threshold: float) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT sku, name, on_hand_qty, sell_through_rate FROM inventory WHERE store=? AND sell_through_rate < ?", (store, threshold))
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "sku": row[0],
            "name": row[1],
            "on_hand_qty": row[2],
            "sell_through_rate": row[3]
        })
    return results

def draft_restock_suggestion(sku: str, store: str) -> dict:
    stock = check_stock_level(sku, store)
    if "error" in stock:
        return stock
        
    diff = stock["reorder_point"] - stock["on_hand_qty"]
    if diff <= 0:
        return {"suggestion": f"No restock needed. On hand ({stock['on_hand_qty']}) is above reorder point ({stock['reorder_point']})."}
    
    draft = f"Subject: Restock Request for SKU {sku} at {store}\n\nHi Team,\n\nWe are currently at {stock['on_hand_qty']} units for SKU {sku}, which is below our reorder point of {stock['reorder_point']}. Given the sell-through rate, please order {diff + 10} units to ensure sufficient days of cover.\n\nThanks,"
    
    return {
        "structured": {
            "sku": sku,
            "store": store,
            "current_qty": stock["on_hand_qty"],
            "suggested_order_qty": diff + 10
        },
        "draft": draft
    }
