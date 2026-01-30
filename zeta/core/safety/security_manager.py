from rich.prompt import Confirm
from typing import Literal
from zeta.core.system.config_manager import ConfigManager
from zeta.core.safety.audit_log import AuditLogger
from zeta.utils.logger import logger

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]

class SecurityManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.audit = AuditLogger(config)
        self.require_confirmation = self.config.get("safety.require_confirmation", True)
        self.risk_tolerance = self.config.get("safety.risk_tolerance", "low").upper()

    def verify_action(self, action_type: str, resource: str, risk_level: RiskLevel) -> bool:
        """
        Determines if an action allowed.
        - LOW risk: Allowed automatically (logs info).
        - MEDIUM risk: Requires confirmation unless tolerance is HIGH.
        - HIGH risk: ALWAYS requires confirmation.
        """
        
        # 1. Determine if we need to ask
        should_ask = False
        
        if risk_level == "HIGH":
            should_ask = True # Always ask for high risk
        elif risk_level == "MEDIUM":
            if self.require_confirmation and self.risk_tolerance != "HIGH":
                should_ask = True
        # LOW is always auto-approved
        
        # 2. Ask user if needed
        approved = True
        if should_ask:
            logger.warning(f"[SECURITY] Action Requested: {action_type}")
            logger.warning(f"           Resource: {resource}")
            logger.warning(f"           Risk Level: {risk_level}")
            
            # Using Typer/Rich for input
            approved = Confirm.ask(f"[bold red]Allow this action?[/bold red]")
            
        # 3. Log it
        self.audit.log_action(action_type, resource, risk_level, approved)
        
        if not approved:
            logger.error(f"Action DENIED by user: {action_type} on {resource}")
        
        return approved
