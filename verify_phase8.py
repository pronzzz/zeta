import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from zeta.core.agent import Agent
from zeta.core.system.config_manager import ConfigManager

def test_intelligence():
    print("\n--- Testing Phase 8: Intelligence (NLU) ---")
    
    config = ConfigManager()
    agent = Agent(config)
    
    # 1. Test Search Intent
    print("\n[Input]: 'Search for the latest news on AGI'")
    response = ""
    for chunk in agent.process("Search for the latest news on AGI"):
        response += chunk
    
    if "Search Results" in response or "blocked by security" in response:
        print("  ✅ Intent Router correctly mapped to SEARCH.")
        print(f"  Response Preview: {response[:100]}...")
    else:
        print("  ❌ Intent Router Failed.")
        print(f"  Response: {response}")

    # 2. Test Greeting (Speed Check)
    print("\n[Input]: 'Hello'")
    response = ""
    for chunk in agent.process("Hello"):
        response += chunk
    
    if "how can I" in response.lower() or "hello" in response.lower():
        print("  ✅ Intent Router handled CHAT correctly.")
    else:
        print("  ⚠️ Chat response unexpected.")

if __name__ == "__main__":
    test_intelligence()
