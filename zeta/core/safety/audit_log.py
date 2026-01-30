import logging
from datetime import datetime
from pathlib import Path
from zeta.core.system.config_manager import ConfigManager

class AuditLogger:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.log_path = Path(self.config.get("system.storage_path", "./storage/data")) / "audit.log"
        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        # Ensure only one handler
        if not self.logger.handlers:
            fh = logging.FileHandler(self.log_path)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def log_action(self, action: str, resource: str, risk: str, approved: bool):
        status = "APPROVED" if approved else "DENIED"
        self.logger.info(f"{status} | Action: {action} | Resource: {resource} | Risk: {risk}")
