import chromadb
from chromadb.config import Settings
from typing import List, Dict
import numpy as np

class ChromaDBStorage:
    def __init__(self, collection_name: str = "code_embeddings"):
        # Khởi tạo client và collection
        self.client = chromadb.Client(Settings())
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, embeddings: np.ndarray, code_blocks: List[Dict]):
        """Thêm embeddings và metadata vào ChromaDB"""
        # Chuyển embeddings sang dạng list để tương thích với ChromaDB
        embeddings_list = embeddings.tolist()
        # Tạo metadata từ code_blocks
        metadatas = [{"path": block["path"], "language": block["language"]} for block in code_blocks]
        # Tạo danh sách ID duy nhất cho mỗi embedding
        ids = [str(i) for i in range(len(code_blocks))]
        # Thêm vào collection
        self.collection.add(embeddings=embeddings_list, metadatas=metadatas, ids=ids)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Tìm kiếm các embedding tương tự"""
        # Chuyển query_embedding sang list
        query_embedding_list = query_embedding.tolist()
        # Truy vấn ChromaDB
        results = self.collection.query(query_embeddings=[query_embedding_list], n_results=k)
        # Trả về kết quả
        return results

    def clear(self):
        """Xóa toàn bộ dữ liệu trong collection"""
        self.collection.delete()
