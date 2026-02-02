"""Create opportunity cards from extracted rules."""
from typing import List
from schemas.opportunities import OpportunityCard


def mine_opportunities(rules) -> List[OpportunityCard]:
    out = []
    for r in rules:
        card = OpportunityCard(id=r.id + "_o1", rule_id=r.id, title=r.summary[:60], description=r.summary)
        out.append(card)
    return out
