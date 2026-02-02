from pydantic import BaseModel
from typing import List, Optional


class Chunk(BaseModel):
    id: str
    text: str
    source: Optional[str]
    metadata: Optional[dict] = {}


class IngestResult(BaseModel):
    chunks: List[Chunk]
    source: Optional[str]
