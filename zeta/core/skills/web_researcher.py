from duckduckgo_search import DDGS
from zeta.core.safety.security_manager import SecurityManager
from typing import Generator

class WebResearcher:
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager

    def search(self, query: str, max_results: int = 3) -> Generator[str, None, None]:
        # Security Check
        if not self.security.verify_action("NETWORK_REQUEST", f"Search: {query}", "MEDIUM"):
            yield "Action blocked by security."
            return

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                if not results:
                    yield f"No results found for '{query}'."
                    return
                
                yield f"Search Results for '{query}':\n"
                for i, r in enumerate(results, 1):
                    yield f"{i}. [{r['title']}]({r['href']})\n   {r['body']}\n\n"
        except Exception as e:
            yield f"Search failed: {e}"
