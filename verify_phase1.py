import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from zeta.core.system.spec_analyzer import SpecAnalyzer
from zeta.core.system.config_manager import ConfigManager
from zeta.utils.crypto import CryptoUtils
from zeta.storage.local import LocalStorage

def test_spec_analyzer():
    print("\n--- Testing Spec Analyzer ---")
    try:
        specs = SpecAnalyzer.get_system_specs()
        print("Specs retrieved successfully:")
        print(f"  Platform: {specs['platform']['system']}")
        print(f"  RAM: {specs['memory']['total_gb']} GB")
        recommendation = SpecAnalyzer.recommend_model(specs)
        print(f"  Recommended Model: {recommendation}")
    except Exception as e:
        print(f"FAILED: {e}")

def test_config_manager():
    print("\n--- Testing Config Manager ---")
    try:
        cm = ConfigManager("test_config.yaml")
        print(f"  Default model: {cm.get('llm.model')}")
        
        # Test save
        cm.config['test_key'] = 'test_value'
        cm.save_config(cm.config)
        
        # Reload
        cm2 = ConfigManager("test_config.yaml")
        if cm2.get('test_key') == 'test_value':
            print("  Config save/load verified.")
        else:
            print("  Config save/load usage FAILED.")
            
        # Cleanup
        os.remove("test_config.yaml")
    except Exception as e:
        print(f"FAILED: {e}")

def test_crypto():
    print("\n--- Testing Crypto ---")
    try:
        crypto = CryptoUtils(key_path="test.key")
        original = "Secret Message"
        encrypted = crypto.encrypt(original)
        decrypted = crypto.decrypt(encrypted)
        
        if original == decrypted:
            print("  Encryption/Decryption verified.")
        else:
            print("  Encryption mismatch.")
            
        # Cleanup
        if os.path.exists("test.key"):
            os.remove("test.key")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    print("Starting Phase 1 Verification...")
    test_spec_analyzer()
    test_config_manager()
    test_crypto()
    print("\nVerification Complete.")
