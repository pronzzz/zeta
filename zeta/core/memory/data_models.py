from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class MemoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    embedding: Optional[List[float]] = None # Vector embedding
    
class ConversationLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str # "user" or "agent"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str

class UserProfile(BaseModel):
    username: str
    preferences: Dict[str, Any] = Field(default_factory=dict)
