from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from pydantic import BaseModel
import uvicorn
import threading

# Import Core Components
from zeta.core.agent import ZetaAgent
from zeta.core.safety.security_manager import RiskLevel

app = FastAPI(title="Zeta API", version="1.0")

# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agent (Singleton)
agent = ZetaAgent()

class ChatRequest(BaseModel):
    message: str

class SkillResponse(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    risk_level: str
    enabled: bool

@app.get("/")
def read_root():
    return {"status": "Zeta is running"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    """Chat endpoint."""
    response = agent.run(request.message)
    return {"response": response}

@app.get("/api/skills", response_model=List[SkillResponse])
def get_skills():
    """Returns list of available skills with risk info."""
    metadata = agent.tool_manager.get_tools_metadata()
    skills = []
    
    for tool in metadata:
        name = tool['name']
        risk = agent.security_manager.assess_risk(name, {})
        
        # In a real app, 'enabled' might be stored in a db
        skills.append({
            "name": name,
            "description": tool['description'],
            "parameters": tool['parameters'],
            "risk_level": risk.value,
            "enabled": True 
        })
    return skills

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
