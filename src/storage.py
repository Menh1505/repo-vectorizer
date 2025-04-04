# src/storage.py
import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict

class FaissStorage:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        
    def add(self, embeddings: np.ndarray, code_blocks: List[Dict]):
        """Add embeddings and metadata to storage"""
        self.index.add(embeddings.astype('float32'))
        self.metadata.extend([{
            'path': block['path'],
            'language': block['language']
        } for block in code_blocks])
        
    def save(self, index_path: str, metadata_path: str):
        """Save index and metadata to files"""
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        
        # Save metadata
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f)
            
    def load(self, index_path: str, metadata_path: str):
        """Load index and metadata from files"""
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
            
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for similar code blocks"""
        distances, indices = self.index.search(
            query_embedding.astype('float32').reshape(1, -1), k
        )
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                results.append({
                    'metadata': self.metadata[idx],
                    'distance': float(distance)
                })
                
        return results