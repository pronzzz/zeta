import subprocess
import sys

def verify():
    print("Verifying Phase 12: Multi-Agent Support-Ticket Triage...")
    
    # 1. Generate tickets
    print("Generating synthetic tickets...")
    result = subprocess.run([sys.executable, "agents/support_triage/tickets_synth.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error generating tickets:\n{result.stderr}")
        return False
    print(result.stdout)
    
    # 2. Run evals to ensure triage pipeline registered correctly
    print("Running evaluations (including Phase 12 tasks)...")
    result_eval = subprocess.run([sys.executable, "main.py", "eval", "run"], capture_output=True, text=True)
    if result_eval.returncode != 0:
        print(f"Error running evals:\n{result_eval.stderr}")
        return False
        
    print(result_eval.stdout)
    
    print("Phase 12 verification complete.")
    return True

if __name__ == "__main__":
    if not verify():
        sys.exit(1)
