"""Opportunities pipeline stub."""
from agents.opportunity_miner_agent import mine_opportunities
from agents.publisher_agent import publish


def run_opportunities_pipeline(rules):
    opportunities = mine_opportunities(rules)
    publish("outputs/opportunities.json", [o.dict() for o in opportunities])
    return opportunities
