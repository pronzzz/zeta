import os
import json

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20):
    """
    Splits text into chunks of `chunk_size` characters with `overlap`.
    Rationale for 100 char chunks: The source material is very dense, line-by-line notes.
    Small chunks preserve the high information density per retrieval hit.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def ingest_documents(filepath: str):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
        
    with open(filepath, 'r') as f:
        text = f.read()
        
    chunks = chunk_text(text, chunk_size=150, overlap=30)
    print(f"Ingested {len(chunks)} chunks from {filepath}")
    return chunks

if __name__ == "__main__":
    chunks = ingest_documents("data/aws_itil_notes.txt")
    with open("data/chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)
