import os
import json
from datetime import datetime
from typing import Dict, Any

class AuditLog:
    LOG_FILE = "./storage/logs/audit.jsonl"

    def __init__(self):
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)

    def log_action(self, tool_name: str, args: Dict[str, Any], risk: str, status: str, user_reason: str = None):
        """Logs an action to the audit file."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "args": args,
            "risk": risk,
            "status": status,  # ALLOWED / DENIED
            "user_reason": user_reason
        }
        
        with open(self.LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
