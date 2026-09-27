class Reviewer:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def review(self, state):
        draft = state["draft"]
        category = state["category"]
        
        # Rule-based guardrails
        if "refund" in draft.lower() and category != "refund":
            return {"final_response": "Draft rejected: Unapproved refund mentioned.", "status": "blocked"}
            
        prompt = f"""
Review this customer support draft for policy compliance.
Draft: {draft}

Does it sound polite and avoid promising unauthorized actions?
Answer YES or NO.
"""
        response = self.model_manager.generate(prompt, stream=False)
        if "YES" in response.upper():
            return {"final_response": draft, "status": "approved"}
        else:
            return {"final_response": f"Draft rejected by reviewer: {response}", "status": "blocked"}
