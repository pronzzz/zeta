from duckduckgo_search import DDGS
from zeta.utils.logger import logger

class WebResearcher:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query: str, max_results: int = 5) -> str:
        """
        Searches the web for the given query.
        Returns a summary of the top results.
        """
        try:
            results = self.ddgs.text(query, max_results=max_results)
            if not results:
                return "No results found."
            
            summary = ""
            for i, res in enumerate(results):
                summary += f"{i+1}. {res['title']}: {res['body']}\nLink: {res['href']}\n\n"
            
            return summary
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"Search failed: {str(e)}"
