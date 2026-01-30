import os
from pathlib import Path
from typing import List, Optional
from zeta.core.system.config_manager import ConfigManager
from zeta.core.safety.security_manager import SecurityManager
from zeta.utils.logger import logger

class FileManager:
    def __init__(self, config: ConfigManager, security_manager: SecurityManager = None):
        self.config = config
        self.security = security_manager
        # Default workspace is ./workspace if not set
        self.workspace_root = Path(self.config.get("system.workspace_path", "./workspace")).resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def _is_safe_path(self, path: Path) -> bool:
        """
        Ensures the path is within the workspace root.
        """
        try:
            full_path = path.resolve()
            return self.workspace_root in full_path.parents or full_path == self.workspace_root
        except Exception:
            return False

    def list_directory(self, relative_path: str = ".") -> List[str]:
        target_path = (self.workspace_root / relative_path).resolve()
        
        if not self._is_safe_path(target_path):
            logger.warning(f"Access denied to path: {target_path}")
            return []
            
        if not target_path.exists() or not target_path.is_dir():
            return []
            
        return [f.name for f in target_path.iterdir()]

    def read_file(self, filename: str) -> Optional[str]:
        target_path = (self.workspace_root / filename).resolve()
        
        if not self._is_safe_path(target_path):
            logger.warning(f"Access denied to file: {target_path}")
            return None
            
        if not target_path.exists() or not target_path.is_file():
            return None
            
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {e}")
            return None

    def write_file(self, filename: str, content: str) -> bool:
        target_path = (self.workspace_root / filename).resolve()
        
        if not self._is_safe_path(target_path):
            logger.warning(f"Access denied to write file: {target_path}")
            return False
            
        # Security Check
        if self.security:
            if not self.security.verify_action("WRITE_FILE", filename, "MEDIUM"):
                return False

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"File written successfully: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to write file {filename}: {e}")
            return False
