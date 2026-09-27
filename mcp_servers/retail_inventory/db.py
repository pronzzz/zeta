import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'inventory.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            name TEXT,
            store TEXT,
            on_hand_qty INTEGER,
            reorder_point INTEGER,
            sell_through_rate REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
