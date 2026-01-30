import requests
from typing import Optional, Dict, Any
from zeta.core.safety.security_manager import SecurityManager
from zeta.utils.logger import logger

class APIManager:
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Optional[requests.Response]:
        """
        Securely performs a GET request after security check.
        """
        # Security Check: Network requests are MEDIUM risk
        if not self.security.verify_action("NETWORK_GET", url, "MEDIUM"):
            return None

        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"API Request Failed ({url}): {e}")
            return None
