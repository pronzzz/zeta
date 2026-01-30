from zeta.core.agent import ZetaAgent
from zeta.utils.logger import setup_logger

def verify_phase3():
    setup_logger()
    print("--- Starting Phase 3 Verification (Agent Loop) ---")
    
    agent = ZetaAgent()
    
    # Test 1: Simple Chat (No Tool)
    print("\n[Test 1] Simple Chat")
    res1 = agent.run("Hello, who are you?")
    print(f"Agent: {res1}")
    
    # Test 2: Tool Usage (Note Taking)
    print("\n[Test 2] Tool Usage (Create Note)")
    res2 = agent.run("Create a note called 'TestNote' with content 'This is a test note from Phase 3 verification.'")
    print(f"Agent: {res2}")
    
    # Test 3: Tool Usage (Web Search) - Mocked logic or real if connected
    # We will trust the LLM's decision to call the tool.
    
if __name__ == "__main__":
    verify_phase3()
