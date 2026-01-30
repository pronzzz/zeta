from typing import List, Dict, Any
from zeta.core.memory.sql_store import SQLStore
from zeta.core.memory.vector_store import VectorStore
from zeta.core.memory.data_models import ConversationLog, MemoryItem
from zeta.core.system.config_manager import ConfigManager
from zeta.utils.logger import logger
import uuid

class MemoryManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.sql_store = SQLStore(config)
        self.vector_store = VectorStore(config)
        self.current_session_id = str(uuid.uuid4())

    def get_context(self, query: str) -> str:
        """
        Builds a context string from:
        1. Recent conversation history (SQL)
        2. Relevant long-term memories (Vector)
        """
        context_parts = []
        
        # 1. Fetch recent history
        history_logs = self.sql_store.get_recent_history(self.current_session_id, limit=5)
        
        # If new session, try to fetch very last interaction from ANY session for continuity
        if not history_logs:
             # This is a simple hack for "Global Recall" on restart
             # In production, we'd query by user_id, but here it's single user
             history_logs = self.sql_store.get_recent_history(None, limit=2)
             if history_logs:
                 context_parts.append("Previous Session Context:")
        
        if history_logs:
            context_parts.append("Recent Conversation:")
            for log in history_logs:
                context_parts.append(f"{log.role.capitalize()}: {log.content}")
        
        # 2. Fetch relevant semantic memories
        relevant_memories = self.vector_store.query_similarity(query, n_results=3)
        if relevant_memories:
            context_parts.append("\nRelevant Information:")
            for mem in relevant_memories:
                context_parts.append(f"- {mem.content}")
                
        return "\n".join(context_parts)

    def save_interaction(self, user_input: str, agent_response: str):
        # 1. Save to SQL (Chronological)
        user_log = ConversationLog(role="user", content=user_input, session_id=self.current_session_id)
        agent_log = ConversationLog(role="agent", content=agent_response, session_id=self.current_session_id)
        
        self.sql_store.log_interaction(user_log)
        self.sql_store.log_interaction(agent_log)
        
        # 2. Save User Input to Vector DB (Semantic)
        # We only save user input for now as "facts" or "queries"
        # In a real system, we'd have a classifier to decide what's worth saving
        memory_item = MemoryItem(
            content=user_input,
            metadata={"type": "conversation", "role": "user", "session_id": self.current_session_id}
        )
        self.vector_store.add_item(memory_item)
