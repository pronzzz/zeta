import sys
import os
import shutil
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from zeta.core.agent import Agent
from zeta.core.system.config_manager import ConfigManager

def test_automation():
    print("\n--- Testing Task Automation (Phase 3) ---")
    
    config = ConfigManager()
    agent = Agent(config)
    
    # 1. Test File Manager (Setup)
    print("Setting up test workspace...")
    workspace = agent.file_manager.workspace_root
    test_file = workspace / "test_doc.txt"
    with open(test_file, "w") as f:
        f.write("Zeta is an advanced AI agent designed for local privacy " * 50) # Long enough to summarize
        
    # 2. Test /ls command
    print("Testing /ls command...")
    for chunk in agent.process("/ls"):
        print(chunk, end="")
        if "test_doc.txt" in chunk:
            print("\n  ✅ File listing successful.")
            
    # 3. Test /summarize command
    print("\nTesting /summarize command...")
    print("  (This requires Ollama running with a model)")
    # We'll just check if it attempts to run without crashing
    try:
        response = ""
        for chunk in agent.process("/summarize test_doc.txt"):
            response += chunk
            print(chunk, end="")
        print("\n  ✅ Summarize command executed without crash.")
    except Exception as e:
        print(f"\n  ❌ Summarize failed: {e}")

    # 4. Test /note command
    print("\nTesting /note command...")
    try:
        response = ""
        for chunk in agent.process("/note Meeting: Discussing Phase 3"):
            response += chunk
        print(response)
        
        # Verify file creation
        notes_dir = workspace / "notes"
        if list(notes_dir.glob("*Meeting*")):
             print("  ✅ Note file created successfully.")
        else:
             print("  ❌ Note file NOT found.")
             
    except Exception as e:
        print(f"\n  ❌ Note taking failed: {e}")

    print("\nAutomation Verification Complete.")

if __name__ == "__main__":
    test_automation()
