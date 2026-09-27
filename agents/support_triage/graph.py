from typing import TypedDict
from langgraph.graph import StateGraph, END
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from zeta.core.system.config_manager import ConfigManager
from zeta.core.llm.model_manager import ModelManager
from rag_tutor.retrievers import Retrievers
from agents.support_triage.classifier import Classifier
from agents.support_triage.drafter import Drafter
from agents.support_triage.reviewer import Reviewer

class AgentState(TypedDict):
    ticket_text: str
    category: str
    draft: str
    final_response: str
    status: str

def build_graph():
    config_mgr = ConfigManager()
    model_manager = ModelManager(config_mgr)
    retriever = Retrievers()
    
    classifier = Classifier(model_manager)
    drafter = Drafter(model_manager, retriever)
    reviewer = Reviewer(model_manager)
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify", classifier.classify)
    workflow.add_node("draft", drafter.draft)
    workflow.add_node("review", reviewer.review)
    
    # Add edges
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "draft")
    workflow.add_edge("draft", "review")
    workflow.add_edge("review", END)
    
    return workflow.compile()

if __name__ == "__main__":
    app = build_graph()
    sample_state = {"ticket_text": "My new monitor is broken."}
    result = app.invoke(sample_state)
    print(result)
