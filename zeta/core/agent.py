from typing import Generator
from zeta.core.llm.model_manager import ModelManager
from zeta.core.memory.memory_manager import MemoryManager
from zeta.core.system.config_manager import ConfigManager
from zeta.core.tools.file_manager import FileManager
from zeta.core.skills.summarizer import Summarizer
from zeta.core.skills.note_taker import NoteTaker
from zeta.core.skills.market_analyst import MarketAnalyst
from zeta.core.skills.web_researcher import WebResearcher
from zeta.core.skills.web_scraper import WebScraper
from zeta.core.system.system_manager import SystemManager
from zeta.core.safety.security_manager import SecurityManager
from zeta.core.brain.intent_router import IntentRouter
from zeta.utils.logger import logger

class Agent:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
        # Security First
        self.security_manager = SecurityManager(self.config)
        
        self.model_manager = ModelManager(self.config)
        self.memory_manager = MemoryManager(self.config)
        
        # Tools & Skills
        self.file_manager = FileManager(self.config, self.security_manager)
        self.summarizer = Summarizer(self.model_manager, self.file_manager)
        self.note_taker = NoteTaker(self.file_manager, self.memory_manager)
        
        self.market_analyst = MarketAnalyst(self.security_manager)
        self.web_researcher = WebResearcher(self.security_manager)
        self.web_scraper = WebScraper(self.security_manager)
        
        # System Control
        self.system_manager = SystemManager(self.security_manager)
        
        # Intelligence
        self.intent_router = IntentRouter(self.model_manager)
        
        self.system_prompt = "You are Zeta, a local, privacy-first AI agent. " \
                           "Answer the user's questions helpfully. " \
                           "Use the provided context to inform your answers."

    def process(self, user_input: str) -> Generator[str, None, None]:
        # Intelligent Routing
        intent, payload = self.intent_router.route(user_input)
        
        logger.info(f"Intent Detected: {intent} (Payload: {payload})")

        # 1. SEARCH
        if intent == "SEARCH":
            if not payload: 
                yield "What would you like me to search for?"
                return
            yield from self.web_researcher.search(payload)
            return

        # 2. STOCK
        if intent == "STOCK":
            yield self.market_analyst.get_stock_price(payload)
            return

        # 3. BROWSE / VISIT
        if intent == "BROWSE":
            content = self.web_scraper.read_page(payload)
            yield f"Content from {payload}:\n\n{content[:2000]}...\n[Truncated]"
            return

        # 4. SYSTEM
        if intent == "SYSTEM":
            # Direct system command execution (Risk High)
            yield self.system_manager.run_command(payload)
            return

        # 5. NOTE
        if intent == "NOTE":
            if ":" in payload:
                title, body = payload.split(":", 1)
            else:
                title = "Quick Note"
                body = payload
            result = self.note_taker.create_note(title.strip(), body.strip())
            yield result
            return
            
        # 6. DIRECT (Legacy / commands)
        if intent == "DIRECT":
            # Basic fallback for direct /commands if router yields DIRECT
            cmd = user_input.lower()
            if cmd.startswith("/ls"):
                files = self.file_manager.list_directory()
                yield "Files in workspace:\n" + "\n".join(files)
                return
            # ... other manual overrides if needed ...

        # 7. CHAT (Default)
        # Verify if it's a direct command escaping the router (e.g. /ls)
        if user_input.startswith("/"):
             # Fallback to legacy handling just in case
             if user_input.startswith("/ls"):
                files = self.file_manager.list_directory()
                yield "Files in workspace:\n" + "\n".join(files)
                return

        context = self.memory_manager.get_context(user_input)
        full_prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nUser: {user_input}\nAgent:"
        
        response_accumulator = ""
        for chunk in self.model_manager.generate(full_prompt):
            response_accumulator += chunk
            yield chunk
            
        self.memory_manager.save_interaction(user_input, response_accumulator)
