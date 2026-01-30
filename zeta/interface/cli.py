import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from zeta.core.system.spec_analyzer import SpecAnalyzer
from zeta.core.system.config_manager import ConfigManager
from zeta.core.llm.model_manager import ModelManager

app = typer.Typer(help="Zeta - Local Autonomous AI Agent")
console = Console()

@app.command()
def status():
    """
    Displays current system status, loaded config, and model connection.
    """
    with console.status("[bold green]Analyzing system..."):
        specs = SpecAnalyzer.get_system_specs()
        config_mgr = ConfigManager()
        model_mgr = ModelManager(config_mgr)
        connection = model_mgr.check_connection()
    
    # System Specs Table
    table = Table(title="System Specifications")
    table.add_column("Component", style="cyan")
    table.add_column("Details", style="magenta")
    
    table.add_row("OS", f"{specs['platform']['system']} {specs['platform']['release']}")
    table.add_row("CPU", f"{specs['cpu']['physical_cores']} Cores ({specs['cpu']['total_cores']} Logical)")
    table.add_row("RAM", f"{specs['memory']['available_gb']}GB available / {specs['memory']['total_gb']}GB total")
    
    console.print(table)
    
    # Status
    console.print(f"\n[bold]Current Model:[/bold] {config_mgr.get('llm.model')}")
    console.print(f"[bold]Ollama Connection:[/bold] {'[green]Active[/green]' if connection else '[red]disconnected[/red]'}")
    
    # Recommendation
    rec_model = SpecAnalyzer.recommend_model(specs)
    console.print(f"\n[dim]Recommended Model for this system: {rec_model}[/dim]")

@app.command()
def start():
    """
    Starts the interactive agent session.
    """
    from zeta.core.agent import Agent

    config_mgr = ConfigManager()
    agent = Agent(config_mgr)
    
    # --- Web UI Auto-Launch ---
    import subprocess
    from pathlib import Path
    import os
    
    # Resolve project root. 
    # file: zeta/interface/cli.py
    # root: agi-magic
    # Logic: .parents[2] since agi-magic/zeta/interface/cli.py
    
    # However, sometimes __file__ might be symlinked or behaving oddly.
    # Let's try multiple strategies.
    current_file = Path(__file__).resolve()
    
    # Strategy 1: Relative to this file
    candidate_root = current_file.parents[2]
    web_script = candidate_root / "start_web.sh"
    
    # Strategy 2: If we are running via main.py in root (zeta alias -> main.py)
    # Then CWD of process might be user home, but main.py is in root.
    # But we are in library code.
    
    if not web_script.exists():
        # Fallback: Check if we are installed in site-packages (not editable) vs source.
        # If specific layout
         rprint(f"[yellow]Debug: Could not find web script at {web_script}[/yellow]")
    
    web_log = candidate_root / "web.log"
    
    if web_script.exists():
        rprint("[bold cyan]Launching Web UI...[/bold cyan]")
        try:
            with open(web_log, "w") as log:
                # Launch in background
                subprocess.Popen([str(web_script)], stdout=log, stderr=log, cwd=candidate_root)
            rprint(f"[dim]Web UI running at http://localhost:5173 (Log: {web_log})[/dim]")
        except Exception as e:
            rprint(f"[yellow]Failed to launch Web UI: {e}[/yellow]")
    else:
        rprint("[yellow]Web UI script not found (start_web.sh)[/yellow]")
    # --------------------------

    if not agent.model_manager.check_connection():
        rprint("[bold red]Error:[/bold red] Cannot connect to Ollama. Is it running?")
        raise typer.Exit(code=1)

    rprint(f"[bold green]Zeta Agent Online[/bold green] (Model: {agent.model_manager.current_model})")
    rprint("[dim]Type 'exit' to quit.[/dim]\n")
    
    while True:
        try:
            user_input = typer.prompt("You")
            if user_input.lower() in ('exit', 'quit'):
                break
            
            # Streaming response
            rprint("[bold blue]Zeta:[/bold blue] ", end="")
            full_response = ""
            for chunk in agent.process(user_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            print() # Newline
            
        except KeyboardInterrupt:
            rprint("\n[yellow]Exiting...[/yellow]")
            break

@app.command()
def setup():
    """
    Initial setup helper.
    """
    rprint("[bold]Zeta Setup[/bold]")
    
    # 1. Check Specs
    specs = SpecAnalyzer.get_system_specs()
    rec_model = SpecAnalyzer.recommend_model(specs)
    rprint(f"Detected System: {specs['cpu']['physical_cores']} cores, {specs['memory']['total_gb']}GB RAM")
    
    confirm = typer.confirm(f"Recommended model is '{rec_model}'. Update config to use this?")
    if confirm:
        cm = ConfigManager()
        cm.config['llm']['model'] = rec_model
        cm.save_config(cm.config)
        rprint(f"[green]Config updated to use {rec_model}.[/green]")
        
        pull = typer.confirm(f"Do you want to pull '{rec_model}' now via Ollama?")
        if pull:
            mm = ModelManager(cm)
            if mm.check_connection():
                mm.pull_model(rec_model)
            else:
                rprint("[red]Ollama not running. Cannot pull model.[/red]")

@app.command()
def version():
    """Print the version."""
    rprint("Zeta v0.1.0-alpha")

if __name__ == "__main__":
    app()
