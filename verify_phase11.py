import subprocess
import sys
import os

def verify():
    print("Verifying Phase 11: RAG Tutor...")
    
    # 1. Ingest Data
    print("Running ingest pipeline...")
    result = subprocess.run([sys.executable, "rag_tutor/ingest.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in ingest:\n{result.stderr}")
        return False
    print(result.stdout)
    
    # 2. Run ablation
    print("Running ablation tests...")
    result_ablation = subprocess.run([sys.executable, "ablation.py"], capture_output=True, text=True, cwd=os.path.join(os.getcwd(), 'rag_tutor'))
    if result_ablation.returncode != 0:
        print(f"Error in ablation:\n{result_ablation.stderr}")
        return False
    print(result_ablation.stdout)
    
    print("Phase 11 verification complete.")
    return True

if __name__ == "__main__":
    if not verify():
        sys.exit(1)
