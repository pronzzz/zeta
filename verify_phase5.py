import requests
import time
import subprocess
import os

def verify_phase5():
    print("--- Starting Phase 5 Verification (Web API) ---")
    
    # 1. Start Backend API in background
    print("[Test 1] Starting Backend API...")
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    # Use a port that is likely free
    api_process = subprocess.Popen(
        ["python3", "-m", "uvicorn", "zeta.server.api:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    try:
        # Wait for server startup
        time.sleep(5)
        
        # 2. Test /api/skills
        print("\n[Test 2] Fetching Skills...")
        try:
            response = requests.get("http://localhost:8001/api/skills")
            
            if response.status_code == 200:
                skills = response.json()
                print(f"✅ SUCCESS: Fetched {len(skills)} skills.")
                print("Skills found:", [s['name'] for s in skills])
                
                # Verify metadata
                if 'risk_level' in skills[0]:
                    print("✅ Metadata 'risk_level' present.")
                else:
                    print("❌ MISSING 'risk_level' in response.")
            else:
                print(f"❌ FAILURE: API returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
             print("❌ FAILURE: Could not connect to API.")

    finally:
        # Cleanup
        print("\nStopping Server...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    verify_phase5()
