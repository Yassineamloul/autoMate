"""Simple in-memory vector index placeholder."""
from typing import List


class VectorIndex:
    def __init__(self):
        self.items = []

    def upsert(self, vectors: List[dict]):
        self.items.extend(vectors)

    def search(self, query_vector, k: int = 5):
        # naive placeholder
        return self.items[:k]
