import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os
from zeta.utils.logger import logger
from zeta.core.memory.data_models import MemoryEntry

class VectorStore:
    def __init__(self, storage_path: str = "./storage/chroma"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=storage_path)
        
        # We'll use a collection for facts/memories
        self.collection = self.client.get_or_create_collection(
            name="zeta_memories",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"VectorStore initialized at {storage_path}")

    def add_memory(self, memory: MemoryEntry):
        """Adds a memory entry to the vector store."""
        try:
            self.collection.add(
                documents=[memory.content],
                metadatas=[{
                    "category": memory.category, 
                    "timestamp": str(memory.timestamp),
                    **memory.metadata
                }],
                ids=[memory.id]
            )
            logger.debug(f"Added memory to vector store: {memory.content[:50]}...")
        except Exception as e:
            logger.error(f"Failed to add memory to vector store: {e}")

    def search_memories(self, query: str, limit: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches for semantically similar memories."""
        try:
            where_filter = {}
            if category:
                where_filter["category"] = category
                
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            memories = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    memories.append({
                        "content": doc,
                        "metadata": metadata,
                        "distance": results["distances"][0][i] if results["distances"] else None
                    })
            
            return memories
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def count(self) -> int:
        return self.collection.count()
