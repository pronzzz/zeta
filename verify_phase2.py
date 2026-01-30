from zeta.core.memory.memory_manager import MemoryManager
from zeta.utils.logger import setup_logger
import time

def verify_memory_system():
    setup_logger()
    print("--- Starting Phase 2 Verification ---")
    
    mm = MemoryManager()
    
    # 1. Test SQL Store (Conversation History)
    print("\n[Test 1] Saving conversation turns...")
    mm.save_turn("user", "Hello Zeta, my name is Pranav.")
    mm.save_turn("assistant", "Hello Pranav! Nice to meet you.")
    
    # 2. Test Vector Store (Long-term Memory)
    print("\n[Test 2] Saving long-term memory...")
    mm.save_memory("User's name is Pranav", category="user_profile")
    mm.save_memory("User likes coding in Python", category="user_profile")
    
    # Allow some time for vector indexing if needed
    time.sleep(1)
    
    # 3. Test Retrieval
    print("\n[Test 3] Retrieving context for 'Who am I?'...")
    context = mm.get_context("Who is Pranav?")
    
    print("\n--- Context Retrieved ---")
    print(f"Recent History: {len(context['history'])} turns")
    print(f"Relevant Memories: {context['memories']}")
    
    if "User's name is Pranav" in context['memories'] or any("Pranav" in m for m in context['memories']):
        print("\n✅ SUCCESS: Retrieved relevant memory!")
    else:
        print("\n❌ FAILURE: Did not retrieve relevant memory.")

if __name__ == "__main__":
    verify_memory_system()
