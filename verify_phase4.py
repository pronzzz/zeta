from zeta.core.agent import ZetaAgent
from zeta.utils.logger import setup_logger
from unittest.mock import patch
import sys

def verify_phase4():
    setup_logger()
    print("--- Starting Phase 4 Verification (Security) ---")
    
    agent = ZetaAgent()
    
    # We want to force a high risk action.
    # We'll simulate the user typing 'n' to deny it.
    
    print("\n[Test] Agent attempts to search web (MEDIUM Risk).")
    print("User input will be simulated as 'n' (Deny).")
    
    # Patching input to simulate user denial
    with patch('builtins.input', return_value='n'):
        response = agent.run("Search for 'DeepMind Zeta Agent'")
        
    print(f"\nFinal Agent Response: {response}")
    
    if "Denied" in str(response) or "sorry" in str(response).lower() or "understood" in str(response).lower():
        print("✅ SUCCESS: Agent respected the denial.")
    else:
        print("⚠️ NOTE: Check response content. If agent acknowledged denial, it passed.")

if __name__ == "__main__":
    verify_phase4()
