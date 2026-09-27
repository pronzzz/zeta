import json
import random

TICKET_TEMPLATES = [
    {"type": "refund", "text": "I bought SKU {sku} but it arrived broken. I want a refund now!"},
    {"type": "escalation", "text": "I've been waiting for 3 days for my restock of {sku} at {store}. I demand to speak to a manager."},
    {"type": "fault", "text": "My new {sku} monitor from {store} is flickering."},
    {"type": "price_match", "text": "I saw SKU {sku} cheaper at a competitor. Can you match it at {store}?"}
]

def generate_tickets(num=10):
    tickets = []
    for i in range(num):
        template = random.choice(TICKET_TEMPLATES)
        sku = str(random.randint(1000, 9999))
        store = random.choice(["Belconnen", "Civic", "Woden"])
        text = template["text"].format(sku=sku, store=store)
        tickets.append({"id": f"TKT-{1000+i}", "type": template["type"], "text": text})
    return tickets

if __name__ == "__main__":
    tickets = generate_tickets()
    with open("data/synthetic_tickets.json", "w") as f:
        json.dump(tickets, f, indent=2)
    print(f"Generated {len(tickets)} synthetic tickets.")
