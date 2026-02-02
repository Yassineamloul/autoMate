"""Publisher agent to save outputs (stub)."""
import json
from pathlib import Path


def publish(path: str, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
