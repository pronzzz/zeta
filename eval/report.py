import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()

def generate_report(db_path="eval_results.db"):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Get overall stats
        c.execute("SELECT COUNT(*) FROM runs")
        total_runs = c.fetchone()[0]
        
        if total_runs == 0:
            console.print("[yellow]No eval runs found in database.[/yellow]")
            return
            
        c.execute("SELECT commit_hash, model, COUNT(*), SUM(passed) FROM runs GROUP BY commit_hash, model ORDER BY timestamp DESC LIMIT 10")
        runs = c.fetchall()
        
        table = Table(title="Evaluation Pass Rates by Commit / Model")
        table.add_column("Commit", style="cyan")
        table.add_column("Model", style="magenta")
        table.add_column("Total Tasks", justify="right")
        table.add_column("Passed", style="green", justify="right")
        table.add_column("Pass Rate", style="blue", justify="right")
        
        for run in runs:
            commit, model, total, passed = run
            pass_rate = (passed / total) * 100 if total > 0 else 0
            table.add_row(commit, model, str(total), str(passed), f"{pass_rate:.1f}%")
            
        console.print(table)
        conn.close()
        
    except sqlite3.OperationalError:
        console.print("[red]Database not found. Run evaluations first.[/red]")

if __name__ == "__main__":
    generate_report()
