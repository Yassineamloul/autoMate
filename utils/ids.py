"""ID generators for chunks and other entities."""
import uuid


def make_chunk_id() -> str:
    return f"chunk_{uuid.uuid4().hex[:8]}"
