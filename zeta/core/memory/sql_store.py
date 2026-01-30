import sqlite3
from typing import List, Optional
from zeta.core.memory.data_models import ConversationLog
from zeta.core.system.config_manager import ConfigManager
from zeta.utils.logger import logger
from datetime import datetime

class SQLStore:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.db_path = self.config.get("system.storage_path", "./storage/data") + "/zeta_memory.db"
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path))
        # Enable WAL mode for concurrency (CLI + Server)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to init SQL DB: {e}")

    def log_interaction(self, log: ConversationLog):
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversation_logs (session_id, role, content)
                VALUES (?, ?, ?)
            """, (log.session_id, log.role, log.content))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")

    def get_recent_history(self, session_id: str = None, limit: int = 5) -> List[ConversationLog]:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        try:
            if session_id:
                cursor.execute("""
                    SELECT role, content, timestamp 
                    FROM conversation_logs 
                    WHERE session_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (session_id, limit))
            else:
                # Global fetch (latest from any session)
                cursor.execute("""
                    SELECT role, content, timestamp 
                    FROM conversation_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
            rows = cursor.fetchall()
            logs = []
            for row in reversed(rows): # Reverse back to chronological order
                logs.append(ConversationLog(
                    role=row[0],
                    content=row[1],
                    session_id=session_id or "unknown"
                ))
            return logs
        except Exception as e:
            logger.error(f"Failed to fetch history: {e}")
            return []
        finally:
            conn.close()
