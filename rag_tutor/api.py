from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add parent to path for retrievers
sys.path.append(os.path.dirname(__file__))
from retrievers import Retrievers

app = FastAPI()
retriever = Retrievers()

class Query(BaseModel):
    text: str
    method: str = "hybrid"

@app.post("/tutor/ask")
def ask_tutor(query: Query):
    if query.method == "keyword":
        chunks = retriever.retrieve_keyword(query.text)
    elif query.method == "dense":
        chunks = retriever.retrieve_dense(query.text)
    else:
        chunks = retriever.retrieve_hybrid(query.text)
        
    return {
        "query": query.text,
        "method": query.method,
        "context": chunks
    }
