from pydantic import BaseModel
from typing import Optional


class OpportunityCard(BaseModel):
    id: str
    rule_id: str
    title: str
    description: str
    estimated_impact: Optional[str]
