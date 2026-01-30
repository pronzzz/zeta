from bs4 import BeautifulSoup
from zeta.core.browser.browser_manager import BrowserManager
from zeta.core.safety.security_manager import SecurityManager

class WebScraper:
    def __init__(self, security_manager: SecurityManager):
        self.browser_manager = BrowserManager(security_manager)

    def read_page(self, url: str) -> str:
        html = self.browser_manager.visit_and_extract(url)
        if not html:
            return "Failed to load page (or blocked by security)."

        soup = BeautifulSoup(html, 'html.parser')
        
        # Cleanup
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text()
        
        # Simple whitespace cleanup
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return clean_text[:10000] # Safe limit
    
    def cleanup(self):
        self.browser_manager.close()
