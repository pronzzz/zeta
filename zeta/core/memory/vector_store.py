try:
    import chromadb
except ImportError:
    chromadb = None

from typing import List, Optional
from zeta.core.memory.data_models import MemoryItem
from zeta.utils.logger import logger
from zeta.core.system.config_manager import ConfigManager
import uuid

class VectorStore:
    def __init__(self, config: ConfigManager):
        if not chromadb:
            logger.error("ChromaDB not installed. Semantic memory disabled.")
            self.client = None
            return

        self.config = config
        self.persist_path = self.config.get("system.storage_path", "./storage/data") + "/vector_db"
        
        try:
            self.client = chromadb.PersistentClient(path=self.persist_path)
            self.collection = self.client.get_or_create_collection(name="zeta_semantic_memory")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.client = None

    def add_item(self, item: MemoryItem):
        if not self.client:
            return

        try:
            self.collection.add(
                documents=[item.content],
                metadatas=[item.metadata],
                ids=[item.id]
            )
        except Exception as e:
            logger.error(f"Failed to add item to vector store: {e}")

    def query_similarity(self, query: str, n_results: int = 3) -> List[MemoryItem]:
        if not self.client:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            items = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    # Reconstruct MemoryItem from result
                    # Note: ChromaDB structure is a bit nested
                    content = results['documents'][0][i]
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    doc_id = results['ids'][0][i]
                    
                    items.append(MemoryItem(
                        id=doc_id,
                        content=content,
                        metadata=metadata
                    ))
            return items
        except Exception as e:
            logger.error(f"Failed to query vector store: {e}")
            return []
