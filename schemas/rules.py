from pydantic import BaseModel
from typing import Optional


class Rule(BaseModel):
    id: str
    chunk_id: str
    summary: str
    obligation: Optional[str]
    severity: Optional[str]
