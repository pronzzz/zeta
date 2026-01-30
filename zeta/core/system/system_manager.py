import subprocess
import shlex
from typing import Optional
from zeta.core.safety.security_manager import SecurityManager
from zeta.utils.logger import logger

class SystemManager:
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager

    def run_command(self, command: str) -> str:
        """
        Executes a shell command.
        Security: This is ALWAYS a HIGH level risk.
        """
        # Explicit HIGH risk override
        if not self.security.verify_action("SYSTEM_EXEC", command, "HIGH"):
            return "Command blocked by security."

        try:
            # We use shell=True for convenience in this agent context, 
            # but rely on the Human-in-the-loop to prevent malicious commands.
            # Capturing output.
            result = subprocess.run(
                command, 
                shell=True, 
                text=True, 
                capture_output=True, 
                timeout=60
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
                
            return output.strip() or "Command executed (no output)."
            
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return f"Command execution failed: {e}"
