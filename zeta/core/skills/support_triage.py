from agents.support_triage.graph import build_graph

class SupportTriage:
    def __init__(self):
        self.pipeline = build_graph()

    def process_ticket(self, ticket_text: str) -> str:
        """Process a customer support ticket using the multi-agent triage pipeline."""
        initial_state = {"ticket_text": ticket_text, "category": "", "draft": "", "final_response": "", "status": ""}
        result = self.pipeline.invoke(initial_state)
        return f"Status: {result.get('status', 'unknown')}\nResponse: {result.get('final_response', 'No response')}"
