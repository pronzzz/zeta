import json
import numpy as np
import os
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

class Retrievers:
    def __init__(self, chunks_path=None):
        if chunks_path is None:
            chunks_path = os.path.join(os.path.dirname(__file__), "../data/chunks.json")
        with open(chunks_path, 'r') as f:
            self.chunks = json.load(f)
            
        # 1. Keyword (BM25)
        tokenized_corpus = [doc.split(" ") for doc in self.chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        # 2. Dense (Sentence-Transformers / all-MiniLM-L6-v2)
        # In a real app we might reuse ChromaDB directly, but for ablation this is clean
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_embeddings = self.encoder.encode(self.chunks)

    def retrieve_keyword(self, query: str, k: int = 3):
        tokenized_query = query.split(" ")
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:k]
        return [self.chunks[i] for i in top_indices]

    def retrieve_dense(self, query: str, k: int = 3):
        query_embedding = self.encoder.encode(query)
        # Cosine similarity
        scores = np.dot(self.chunk_embeddings, query_embedding) / (
            np.linalg.norm(self.chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(scores)[::-1][:k]
        return [self.chunks[i] for i in top_indices]

    def retrieve_hybrid(self, query: str, k: int = 3):
        # Reciprocal Rank Fusion (RRF)
        tokenized_query = query.split(" ")
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_ranks = np.argsort(np.argsort(bm25_scores)[::-1])
        
        query_embedding = self.encoder.encode(query)
        dense_scores = np.dot(self.chunk_embeddings, query_embedding) / (
            np.linalg.norm(self.chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        dense_ranks = np.argsort(np.argsort(dense_scores)[::-1])
        
        # RRF formula: 1 / (60 + rank)
        rrf_scores = (1 / (60 + bm25_ranks)) + (1 / (60 + dense_ranks))
        top_indices = np.argsort(rrf_scores)[::-1][:k]
        
        return [self.chunks[i] for i in top_indices]
