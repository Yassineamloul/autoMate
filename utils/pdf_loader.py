"""PDF loader: returns text content of local PDF file."""
from pathlib import Path

def load_pdf(path: str) -> str:
    p = Path(path)
    # For the demo we allow reading plain text files with .pdf extension
    return p.read_text(encoding="utf-8")
