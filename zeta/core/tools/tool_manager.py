from typing import Dict, Callable, Any, List
from pydantic import BaseModel
import inspect
from zeta.utils.logger import logger

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.schemas: List[ToolDefinition] = []

    def register_tool(self, name: str, func: Callable, description: str = None):
        """Registers a Python function as a tool."""
        self.tools[name] = func
        
        # Simple schema generation (In a real scenario, use Pydantic introspection)
        sig = inspect.signature(func)
        params = {}
        for param_name, param in sig.parameters.items():
            params[param_name] = str(param.annotation)
            
        schema = ToolDefinition(
            name=name,
            description=description or func.__doc__ or "No description",
            parameters=params
        )
        self.schemas.append(schema)
        logger.debug(f"Registered tool: {name}")

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return [s.model_dump() for s in self.schemas]
        
    def get_tools_metadata(self) -> List[Dict[str, Any]]:
        """Returns rich metadata for UI."""
        return [s.model_dump() for s in self.schemas]

    def execute_tool(self, name: str, **kwargs) -> Any:
        if name not in self.tools:
            logger.error(f"Tool {name} not found.")
            return f"Error: Tool {name} not found."
        
        try:
            logger.info(f"Executing tool: {name} with args: {kwargs}")
            result = self.tools[name](**kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Error executing {name}: {str(e)}"
