from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import asyncio
from zeta.core.agent import Agent
from zeta.core.system.config_manager import ConfigManager
from zeta.utils.logger import logger

# Initialize App & Agent
app = FastAPI(title="Zeta Web API", description="Backend for Zeta Agent One UI")

# CORS (Allow local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, restrict to localhost:3000/5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = ConfigManager()
agent = Agent(config)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "Zeta Online", "version": "1.0"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Process a user message and return the agent's response.
    Non-streaming for V1 simplicity.
    """
    user_input = request.message
    try:
        # Agent.process returns a generator. We'll consume it fully.
        full_response = ""
        for chunk in agent.process(user_input):
            full_response += chunk
        
        return {"response": full_response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    """
    Fetch recent conversation history from Memory.
    """
    try:
        # Assuming we can access SQLStore securely
        # Using a slight hack to get global history via the private method we added
        logs = agent.memory_manager.sql_store.get_recent_history(None, limit=20)
        return [
            {"role": log.role, "content": log.content, "timestamp": log.timestamp}
            for log in reversed(logs)
        ]
    except Exception as e:
        logger.error(f"History error: {e}")
        return []

@app.get("/stats")
def get_stats():
    """
    Returns system stats and agent memory count.
    """
    from zeta.core.system.spec_analyzer import SpecAnalyzer
    try:
        specs = SpecAnalyzer.get_system_specs()
        # Count memories
        conn = agent.memory_manager.sql_store._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversation_logs")
        count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "cpu_cores": specs['cpu']['physical_cores'],
            "ram_total": specs['memory']['total_gb'],
            "memory_count": count,
            "model": agent.model_manager.current_model
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return {"error": str(e)}

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
