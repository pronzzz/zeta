import subprocess
import sys

def verify():
    print("Verifying Phase 9: Evaluation Harness...")
    
    # Check eval run
    print("Running evaluations...")
    result = subprocess.run([sys.executable, "main.py", "eval", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running evals:\n{result.stderr}")
        return False
    print(result.stdout)
    
    # Check eval report
    print("Running report...")
    result_report = subprocess.run([sys.executable, "main.py", "eval", "report"], capture_output=True, text=True)
    if result_report.returncode != 0:
        print(f"Error running report:\n{result_report.stderr}")
        return False
    print(result_report.stdout)
    
    print("Phase 9 verification complete.")
    return True

if __name__ == "__main__":
    if not verify():
        sys.exit(1)
