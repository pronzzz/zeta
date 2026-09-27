class Drafter:
    def __init__(self, model_manager, retriever):
        self.model_manager = model_manager
        self.retriever = retriever

    def draft(self, state):
        ticket_text = state["ticket_text"]
        category = state["category"]
        
        # Retrieve context relevant to ticket
        context_chunks = self.retriever.retrieve_hybrid(ticket_text, k=2)
        context = "\n".join(context_chunks)
        
        prompt = f"""
Draft a customer support reply for this ticket.
Ticket Category: {category}
Ticket text: {ticket_text}

Relevant Info:
{context}

Keep it brief, polite, and professional. Do NOT promise refunds if you are not authorized.
"""
        draft_text = self.model_manager.generate(prompt, stream=False).strip()
        return {"draft": draft_text}
