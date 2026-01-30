import psutil
import platform
import shutil
from typing import Dict, Any

class SpecAnalyzer:
    @staticmethod
    def get_system_specs() -> Dict[str, Any]:
        """
        Gathers system specifications:
        - RAM (Total, Available)
        - CPU (Cores, Usage)
        - Platform (OS, Arch)
        """
        mem = psutil.virtual_memory()
        
        specs = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python_version": platform.python_version()
            },
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                # "freq": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown" # Can fail on M1/M2 sometimes
            },
            "memory": {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "percent_used": mem.percent
            },
            "disk": {
                "total_gb": round(shutil.disk_usage("/").total / (1024 ** 3), 2),
                "free_gb": round(shutil.disk_usage("/").free / (1024 ** 3), 2)
            }
        }
        
        return specs

    @staticmethod
    def recommend_model(specs: Dict[str, Any]) -> str:
        """
        Recommends a model based on system resources.
        
        Logic:
        - < 8GB RAM: tinyllama, phi or gemma:2b
        - 8GB - 16GB RAM: llama3:8b, mistral
        - > 16GB RAM: mixtral, llama3:70b (if very high)
        """
        total_ram = specs["memory"]["total_gb"]
        
        if total_ram < 8:
            return "tinyllama"
        elif 8 <= total_ram < 16:
            return "llama3:8b" # Standard for most MacBooks
        elif 16 <= total_ram < 32:
            return "mistral"
        else:
            return "mixtral" # Capable of running larger models

if __name__ == "__main__":
    import json
    analyzer = SpecAnalyzer()
    print(json.dumps(analyzer.get_system_specs(), indent=4))
    print(f"Recommended Model: {analyzer.recommend_model(analyzer.get_system_specs())}")
