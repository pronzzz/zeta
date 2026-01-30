from datetime import datetime
from typing import List, Dict, Any, Optional
from zeta.core.memory.vector_store import VectorStore
from zeta.core.memory.sql_store import SQLStore
from zeta.core.memory.data_models import MemoryEntry, ConversationTurn
from zeta.utils.logger import logger
import json

class MemoryManager:
    def __init__(self):
        self.vector_store = VectorStore()
        self.sql_store = SQLStore()
        self.current_session_id = f"session_{int(datetime.now().timestamp())}"
        logger.info(f"MemoryManager initialized. Session ID: {self.current_session_id}")

    def save_turn(self, role: str, content: str, metadata: Dict[str, Any] = {}):
        """Saves a conversation turn to SQL Store."""
        turn = ConversationTurn(
            role=role,
            content=content,
            metadata=metadata
        )
        self.sql_store.log_turn(turn, self.current_session_id)

    def save_memory(self, content: str, category: str = "general", metadata: Dict[str, Any] = {}):
        """Saves a specific fact/memory to Vector Store."""
        memory = MemoryEntry(
            content=content,
            category=category,
            metadata=metadata
        )
        self.vector_store.add_memory(memory)

    def get_context(self, query: str) -> Dict[str, Any]:
        """
        Retrieves context for the LLM.
        - Recent conversation history (Short-term memory)
        - Relevant semantic memories (Long-term memory)
        """
        # 1. Get recent conversation
        recent_history = self.sql_store.get_recent_conversation(limit=10)
        
        # 2. Get relevant long-term memories
        relevant_memories = self.vector_store.search_memories(query, limit=3)
        
        return {
            "history": recent_history,
            "memories": [m["content"] for m in relevant_memories]
        }
    
    def search_long_term(self, query: str):
        return self.vector_store.search_memories(query)

    def close(self):
        self.sql_store.close()
