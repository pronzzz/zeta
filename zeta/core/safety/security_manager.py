from typing import Dict, Any, List
from enum import Enum
from zeta.utils.logger import logger

class RiskLevel(Enum):
    SAFE = "SAFE"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class SecurityManager:
    # Define tool risk profiles
    TOOL_RISKS = {
        "read_note": RiskLevel.SAFE,
        "list_notes": RiskLevel.SAFE,
        "list_dir": RiskLevel.SAFE,
        "read_file": RiskLevel.SAFE,
        "create_note": RiskLevel.MEDIUM,
        "search_web": RiskLevel.MEDIUM,  # Privacy concern?
        # Future tools
        "delete_file": RiskLevel.HIGH,
        "execute_command": RiskLevel.HIGH,
    }

    def __init__(self, risk_tolerance: str = "SAFE"):
        # risk_tolerance: The highest risk level allowed WITHOUT confirmation.
        # Defaults to SAFE, meaning Medium/High require confirmation.
        self.risk_tolerance = self._parse_level(risk_tolerance)

    def _parse_level(self, level_str: str) -> RiskLevel:
        try:
            return RiskLevel[level_str.upper()]
        except KeyError:
            return RiskLevel.SAFE

    def assess_risk(self, tool_name: str, args: Dict[str, Any]) -> RiskLevel:
        """Determines the risk level of a tool call."""
        level = self.TOOL_RISKS.get(tool_name, RiskLevel.HIGH) # Default to HIGH if unknown
        logger.debug(f"Risk assessment for {tool_name}: {level.value}")
        return level

    def requires_confirmation(self, tool_name: str, args: Dict[str, Any]) -> bool:
        """Returns True if the action needs user approval."""
        risk = self.assess_risk(tool_name, args)
        
        # Logic: If Risk > Tolerance -> Confirm
        # Hierarchy: SAFE < MEDIUM < HIGH
        risk_values = {RiskLevel.SAFE: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2}
        
        return risk_values[risk] > risk_values[self.risk_tolerance]
