from playwright.sync_api import sync_playwright, Page, Browser
from typing import Optional
from zeta.core.safety.security_manager import SecurityManager
from zeta.utils.logger import logger

class BrowserManager:
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager
        self.playwright = None
        self.browser: Optional[Browser] = None

    def _start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            # Launch headless by default
            self.browser = self.playwright.chromium.launch(headless=True)

    def visit_and_extract(self, url: str) -> Optional[str]:
        # Security Check
        if not self.security.verify_action("NETWORK_REQUEST", f"Visit: {url}", "MEDIUM"):
            return None

        try:
            self._start()
            page = self.browser.new_page()
            page.goto(url, timeout=30000)
            
            # Simple Text Extraction
            content = page.content()
            page.close()
            return content
        except Exception as e:
            logger.error(f"Browser action failed ({url}): {e}")
            return None

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
