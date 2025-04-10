import chromadb
from chromadb.config import Settings
from typing import List, Dict
import numpy as np

class ChromaDBStorage:
    def __init__(self, collection_name: str = "code_embeddings"):
        # Khởi tạo client và collection
        self.client = chromadb.Client(Settings(
            persist_directory="./chromadb_data",  # data store directory
            chroma_db_impl="duckdb+parquet"      # Use DuckDB to store data in Parquet format
        ))
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, embeddings: np.ndarray, code_blocks: List[Dict]):
        # Convert embeddings to list
        embeddings_list = embeddings.tolist()
        # Generate metadata from code_blocks
        metadatas = [{"path": block["path"], "language": block["language"]} for block in code_blocks]
        # Create unique ID list for each embedding
        ids = [str(i) for i in range(len(code_blocks))]
        # Adding to collection
        self.collection.add(embeddings=embeddings_list, metadatas=metadatas, ids=ids)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        # Convert query_embedding to list
        query_embedding_list = query_embedding.tolist()
        # Query ChromaDB
        results = self.collection.query(query_embeddings=[query_embedding_list], n_results=k)
        # Return results
        return results

    def clear(self):
        self.collection.delete()
