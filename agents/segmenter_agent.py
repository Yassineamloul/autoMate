"""Segmenter agent: splits text into chunks."""
from typing import List
from utils.text_cleaning import clean_text
from utils.ids import make_chunk_id


def segment_text(text: str, source: str = None) -> List[dict]:
    text = clean_text(text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for i, p in enumerate(paragraphs):
        chunks.append({"id": make_chunk_id(), "text": p, "source": source})
    return chunks
