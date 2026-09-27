class Classifier:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def classify(self, state):
        ticket_text = state["ticket_text"]
        prompt = f"Classify this ticket into one of [refund, escalation, fault, price_match]. Just the category word.\nTicket: {ticket_text}"
        category = self.model_manager.generate(prompt, stream=False).strip().lower()
        
        # fallback
        valid = ["refund", "escalation", "fault", "price_match"]
        if not any(c in category for c in valid):
            category = "fault"
            
        return {"category": category}
