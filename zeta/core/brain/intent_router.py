import json
from typing import Optional, Tuple
from zeta.core.llm.model_manager import ModelManager

class IntentRouter:
    def __init__(self, model_manager: ModelManager):
        self.mm = model_manager
        # Brief, strict prompt for classification
        self.router_prompt = """
You are an Intent Classifier for an AI Agent.
Analyze the User Input and map it to one of these internal commands:

1. SEARCH (Web search): User wants news, facts, current events.
   -> Output format: SEARCH: <query>
2. STOCK (Finance): User wants stock price/data.
   -> Output format: STOCK: <symbol>
3. BROWSE (Deep reading): User gives a URL to read/summarize.
   -> Output format: BROWSE: <url>
4. SYSTEM (Terminal): User wants to install/update/run system commands.
   -> Output format: SYSTEM: <shell_command>
   *NOTE*: Convert natural language to the likely shell command (e.g. "update packages" -> "sudo apt update" or "brew upgrade").
5. NOTE (Memory): User explicitly asks to save a note/reminder.
   -> Output format: NOTE: <title>: <content>
6. CHAT: General conversation, greetings, questions about previous context.
   -> Output format: CHAT

User Input: "{input}"

Reply ONLY with the single line output format. No explanations.
"""

    def route(self, user_input: str) -> Tuple[str, str]:
        """
        Returns (Command_Type, Payload)
        """
        # Optimized for speed: if it looks like a direct command, skip LLM
        if user_input.startswith("/"):
            return "DIRECT", user_input

        # fast check for greeting
        if len(user_input.split()) < 2 and user_input.lower() in ["hi", "hello", "hey"]:
            return "CHAT", ""

        try:
            prompt = self.router_prompt.replace("{input}", user_input)
            response = ""
            # We assume model_manager.generate returns a generator
            for chunk in self.mm.generate(prompt):
                 response += chunk
            
            response = response.strip()
            
            if response.startswith("SEARCH:"):
                return "SEARCH", response[7:].strip()
            elif response.startswith("STOCK:"):
                return "STOCK", response[6:].strip()
            elif response.startswith("BROWSE:"):
                return "BROWSE", response[7:].strip()
            elif response.startswith("SYSTEM:"):
                return "SYSTEM", response[7:].strip()
            elif response.startswith("NOTE:"):
                return "NOTE", response[5:].strip()
            else:
                return "CHAT", ""
                
        except Exception:
            return "CHAT", ""
