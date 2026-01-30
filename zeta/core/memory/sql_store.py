import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from zeta.utils.logger import logger
from zeta.core.memory.data_models import ConversationTurn, ConversationSession

class SQLStore:
    def __init__(self, db_path: str = "./storage/zeta.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
        logger.info(f"SQLStore connected to {db_path}")

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                role TEXT,
                content TEXT,
                timestamp TEXT,
                session_id TEXT,
                metadata TEXT
            )
        ''')
        
        # Commands history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                status TEXT,
                timestamp TEXT,
                details TEXT
            )
        ''')
        
        self.conn.commit()

    def log_turn(self, turn: ConversationTurn, session_id: str):
        """Logs a single conversation turn."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (id, role, content, timestamp, session_id, metadata) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    turn.id, 
                    turn.role, 
                    turn.content, 
                    str(turn.timestamp), 
                    session_id, 
                    json.dumps(turn.metadata)
                )
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log conversation turn: {e}")

    def get_recent_conversation(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves the most recent conversation turns."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT role, content, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            # Return in chronological order (oldest -> newest) for context window
            return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows][::-1]
        except Exception as e:
            logger.error(f"Failed to retrieve conversation: {e}")
            return []

    def close(self):
        self.conn.close()
