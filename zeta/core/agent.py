from zeta.core.system.config_manager import ConfigManager
from zeta.core.llm.model_manager import ModelManager
from zeta.core.memory.memory_manager import MemoryManager
from zeta.core.tools.tool_manager import ToolManager
from zeta.core.skills.web_researcher import WebResearcher
from zeta.core.skills.note_taker import NoteTaker
from zeta.core.tools.system_tool import SystemTool
from zeta.core.safety.security_manager import SecurityManager
from zeta.core.safety.audit_log import AuditLog
from zeta.utils.logger import logger
from zeta.core.skills.mcp_retail_client import RetailMCPClient
from zeta.core.skills.support_triage import SupportTriage
import json

class ZetaAgent:
    def __init__(self):
        self.config = ConfigManager()
        self.model_manager = ModelManager(self.config)
        self.memory_manager = MemoryManager()
        self.tool_manager = ToolManager()
        
        # Register Skills
        self.web_researcher = WebResearcher()
        self.note_taker = NoteTaker()
        self.system = SystemTool()
        self.retail_mcp = RetailMCPClient()
        self.triage = SupportTriage()
        
        self.tool_manager.register_tool("search_web", self.web_researcher.search_web)
        self.tool_manager.register_tool("create_note", self.note_taker.create_note)
        self.tool_manager.register_tool("read_note", self.note_taker.read_note)
        self.tool_manager.register_tool("list_notes", self.note_taker.list_notes)
        self.tool_manager.register_tool("list_dir", self.system.list_dir)
        self.tool_manager.register_tool("read_file", self.system.read_file)
        self.tool_manager.register_tool("check_stock_level", self.retail_mcp.check_stock_level)
        self.tool_manager.register_tool("flag_slow_movers", self.retail_mcp.flag_slow_movers)
        self.tool_manager.register_tool("draft_restock_suggestion", self.retail_mcp.draft_restock_suggestion)
        self.tool_manager.register_tool("process_ticket", self.triage.process_ticket)

        # Security
        self.security_manager = SecurityManager(risk_tolerance=self.config.get("safety.risk_tolerance", "SAFE"))
        self.audit_log = AuditLog()

    def run(self, user_input: str) -> str:
        """
        Main Agent Loop:
        1. Retrieve Context
        2. Plan (Thought)
        3. Act (Tool Call) or Answer
        """
        logger.info(f"User Input: {user_input}")
        
        # 1. Retrieve Context
        context_data = self.memory_manager.get_context(user_input)
        history_str = "\n".join([f"{t['role']}: {t['content']}" for t in context_data['history']])
        memories_str = "\n".join(context_data['memories'])
        
        tools_schema = json.dumps(self.tool_manager.get_tool_schemas(), indent=2)

        # 2. Construct Prompt (ReAct Style)
        prompt = f"""
You are Zeta, an autonomous local AI agent.
Your goal is to help the user by using the available tools.

TOOLS AVAILABLE:
{tools_schema}

CONTEXT (Long-term Memories):
{memories_str}

CONVERSATION HISTORY:
{history_str}

USER INPUT: {user_input}

INSTRUCTIONS:
- If you need to use a tool, respond with a JSON object: {{"tool": "tool_name", "args": {{...}}}}
- If you can answer directly, just respond with the answer.
- Do NOT make up facts. Use the tools.
"""

        # 3. Call LLM
        response = self.model_manager.generate(prompt, stream=False)
        logger.info(f"LLM Response: {response}")

        # 4. Check for Tool Call (Simple Heuristic for V1)
        # In a real system, we'd use function calling API or strict JSON parsing
        try:
            if "{" in response and "}" in response and "tool" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                tool_call = json.loads(json_str)
                
                tool_name = tool_call.get("tool")
                args = tool_call.get("args", {})
                
                # --- SECURITY CHECK ---
                risk = self.security_manager.assess_risk(tool_name, args)
                if self.security_manager.requires_confirmation(tool_name, args):
                    # For CLI interaction, we'll simply print and ask for input
                    # In a real async/web app, this would need a callback system or state machine
                    print(f"\n[⚠️ SECURITY ALERT] Agent wants to execute: {tool_name}")
                    print(f"Arguments: {args}")
                    print(f"Risk Level: {risk.value}")
                    user_approval = input(">>> Allow this action? (y/n): ").strip().lower()
                    
                    if user_approval != 'y':
                        print("🚫 Action Denied.")
                        self.audit_log.log_action(tool_name, args, risk.value, "DENIED", "User declined")
                        
                        # Feed denial back to LLM
                        denial_prompt = f"""
{prompt}

AGENT ACTION: Performed security check for {tool_name}.
OBSERVATION: User DENIED the action.
"""
                        final_response = self.model_manager.generate(denial_prompt, stream=False)
                        self.memory_manager.save_turn("user", user_input)
                        self.memory_manager.save_turn("assistant", final_response, metadata={"tool_denied": tool_name})
                        return final_response

                # If Approved or Safe
                self.audit_log.log_action(tool_name, args, risk.value, "ALLOWED")
                
                # Execute Tool
                tool_result = self.tool_manager.execute_tool(tool_name, **args)
                
                # Feed result back to LLM
                follow_up_prompt = f"""
{prompt}

AGENT ACTION: Called {tool_name} with {args}
Observation: {tool_result}

Final Answer:
"""
                final_response = self.model_manager.generate(follow_up_prompt, stream=False)
                
                # Save Interaction
                self.memory_manager.save_turn("user", user_input)
                self.memory_manager.save_turn("assistant", final_response, metadata={"tool_used": tool_name})
                
                return final_response

            else:
                # Direct Answer
                self.memory_manager.save_turn("user", user_input)
                self.memory_manager.save_turn("assistant", response)
                return response

        except Exception as e:
            logger.error(f"Error in Agent Loop: {e}")
            return f"I encountered an error: {e}"
