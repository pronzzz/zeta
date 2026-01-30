import sys
import os
import shutil
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from zeta.core.memory.memory_manager import MemoryManager
from zeta.core.system.config_manager import ConfigManager
from zeta.core.memory.data_models import ConversationLog

def test_memory_system():
    print("\n--- Testing Memory System ---")
    
    # Setup test config
    config = ConfigManager()
    # Use a separate test DB path if possible, but for now we use default
    # creating a temporary config might be cleaner but let's stick to simple integration test
    
    mm = MemoryManager(config)
    session_id = mm.current_session_id
    print(f"Session ID: {session_id}")
    
    # 1. Test Saving Interaction
    user_input = "My favorite programming language is Python."
    agent_response = "That's great! Python is very versatile."
    
    print("Saving interaction...")
    mm.save_interaction(user_input, agent_response)
    
    # 2. Test SQL Retrieval (History)
    print("Testing SQL History Retrieval...")
    history = mm.sql_store.get_recent_history(session_id)
    if len(history) >= 2:
        print("  ✅ SQL History retrieved successfully.")
        print(f"  Last User Input: {history[-2].content}")
    else:
        print("  ❌ SQL History retrieval failed.")

    # 3. Test Vector Retrieval (Context)
    # ChromaDB updates might take a split second, or be immediate. 
    # We'll try to query for "programming language"
    print("Testing Vector Context Retrieval...")
    query = "What do I like to code in?"
    context = mm.get_context(query)
    
    print(f"Context retrieved:\n{context}")
    
    if "Python" in context:
        print("  ✅ Semantic retrieval successful (found 'Python').")
    else:
        print("  ⚠️ Semantic retrieval might be delayed or failed.")

    print("\nMemory System Verification Complete.")

if __name__ == "__main__":
    if "chromadb" not in sys.modules:
        import chromadb # Just to ensure it loads
        print(f"ChromaDB Version: {chromadb.__version__}")
        
    test_memory_system()
