import yaml
import os
from pathlib import Path
from typing import Dict, Any
from zeta.utils.logger import logger

class ConfigManager:
    # Get Project Root (3 levels up from this file: zeta/core/system/config_manager.py -> project_root)
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    
    DEFAULT_CONFIG = {
        "system": {
            "log_level": "INFO",
            "storage_path": str(PROJECT_ROOT / "storage/data"),
            "encryption_enabled": True
        },
        "llm": {
            "model": "llama3:8b",
            "host": "http://localhost:11434",
            "timeout": 30
        },
        "safety": {
            "require_confirmation": True,
            "risk_tolerance": "low"
        }
    }

    def __init__(self, config_path: str = "config.yaml"):
        # Resolve config path relative to project root if not absolute
        path = Path(config_path)
        if not path.is_absolute():
             self.config_path = self.PROJECT_ROOT / config_path
        else:
             self.config_path = path
             
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            logger.info(f"Config file not found at {self.config_path}. Creating default.")
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG

        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or self.DEFAULT_CONFIG
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG

    def save_config(self, config: Dict[str, Any]):
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self.config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default
