"""Embedding helper (stub)."""
from typing import List


def embed_texts(texts: List[str]):
    # Return dummy vectors (length 3) for demo
    return [[float(len(t) % 10), 0.0, 0.0] for t in texts]
