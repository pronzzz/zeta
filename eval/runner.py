import yaml
import sqlite3
import datetime
import subprocess
from pathlib import Path
from rich.console import Console

from zeta.core.agent import ZetaAgent
from zeta.core.system.config_manager import ConfigManager
from eval.grader import Grader

console = Console()

class EvalRunner:
    def __init__(self, db_path="eval_results.db"):
        self.db_path = db_path
        self.config_mgr = ConfigManager()
        self.agent = ZetaAgent()
        # Security manager requires approval for risky tools. 
        # For eval, we temporarily lower risk to allow automated testing, 
        # or we mock the security manager.
        self.agent.security_manager.risk_tolerance = "HIGH" 
        
        self.grader = Grader(self.agent.model_manager)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS runs
                     (timestamp TEXT, commit_hash TEXT, model TEXT, task_id TEXT, 
                      passed BOOLEAN, reason TEXT)''')
        conn.commit()
        conn.close()

    def get_commit_hash(self):
        try:
            return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
        except Exception:
            return "unknown"

    def run_evals(self, tasks_file="eval/tasks/tasks.yaml"):
        with open(tasks_file, 'r') as f:
            data = yaml.safe_load(f)
        
        tasks = data.get('tasks', [])
        commit_hash = self.get_commit_hash()
        model_name = self.config_mgr.get("llm.model")
        
        console.print(f"[bold cyan]Running {len(tasks)} eval tasks...[/bold cyan]")
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        passed_count = 0
        for task in tasks:
            console.print(f"Running Task {task['id']}: {task['input']}")
            
            # Reset memory for independent testing
            self.agent.memory_manager.history = []
            
            response = self.agent.run(task['input'])
            
            # Retrieve metadata from memory manager's last turn
            history = self.agent.memory_manager.get_context("")['history']
            last_metadata = {}
            if history and "metadata" in history[-1]:
                last_metadata = history[-1]["metadata"]
                
            passed, reason = self.grader.grade(task, response, last_metadata)
            
            status = "[green]PASS[/green]" if passed else f"[red]FAIL[/red] ({reason})"
            console.print(f"  Result: {status}")
            
            if passed:
                passed_count += 1
                
            c.execute("INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?)",
                      (datetime.datetime.now().isoformat(), commit_hash, model_name, 
                       str(task['id']), passed, reason))
        
        conn.commit()
        conn.close()
        
        console.print(f"[bold]Total Pass Rate: {passed_count}/{len(tasks)} ({(passed_count/len(tasks))*100:.1f}%)[/bold]")
