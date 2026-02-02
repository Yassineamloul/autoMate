"""Ingest pipeline: load -> segment -> index -> save chunks."""
from agents.ingestion_agent import ingest_document
from agents.segmenter_agent import segment_text
from agents.publisher_agent import publish
from pathlib import Path
import json


def run_ingest_demo():
    # Very small demo: read demo text file
    demo_path = Path(__file__).parent.parent / "demo" / "sample_policies" / "employee_handbook.pdf"
    text = ingest_document(lambda: demo_path.read_text(encoding="utf-8"))
    chunks = segment_text(text, source=str(demo_path))
    out_path = Path(__file__).parent.parent / "outputs" / "chunks.json"
    publish(str(out_path), chunks)
    print(f"Wrote {len(chunks)} chunks to {out_path}")
