from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    category: str = "general"  # fact, preference, episodic, skill
    tags: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)
    embedding_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

class ConversationTurn(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}

class ConversationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = Field(default_factory=datetime.now)
    turns: List[ConversationTurn] = []
    summary: Optional[str] = None
