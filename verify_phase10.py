import subprocess
import sys

def verify():
    print("Verifying Phase 10: MCP Server for Retail Inventory...")
    
    # 1. Seed the database
    print("Seeding synthetic data...")
    result = subprocess.run([sys.executable, "mcp_servers/retail_inventory/seed_data.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error seeding data:\n{result.stderr}")
        return False
    print(result.stdout)
    
    # 2. Run evals to ensure MCP client registered correctly
    print("Running evaluations (including Phase 10 tasks)...")
    result_eval = subprocess.run([sys.executable, "main.py", "eval", "run"], capture_output=True, text=True)
    if result_eval.returncode != 0:
        print(f"Error running evals:\n{result_eval.stderr}")
        return False
        
    print(result_eval.stdout)
    
    print("Phase 10 verification complete.")
    return True

if __name__ == "__main__":
    if not verify():
        sys.exit(1)
