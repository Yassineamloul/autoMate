"""Rule extraction from chunks (stub)."""
from typing import List
from schemas.rules import Rule


def extract_rules_from_chunk(chunk) -> List[Rule]:
    # Placeholder extraction logic
    rule = Rule(id=chunk["id"] + "_r1", chunk_id=chunk["id"], summary=chunk["text"][:120], obligation=None, severity=None)
    return [rule]
