"""Rules pipeline: segments -> rules -> workflow -> simulate."""
from agents.rule_extraction_agent import extract_rules_from_chunk
from agents.opportunity_miner_agent import mine_opportunities
from agents.workflow_generator import generate_workflow
from agents.publisher_agent import publish


def run_rules_pipeline(chunks):
    rules = []
    for c in chunks:
        rules.extend(extract_rules_from_chunk(c))
    opportunities = mine_opportunities(rules)
    workflow = generate_workflow(opportunities)
    publish("outputs/rules.json", [r.dict() for r in rules])
    publish("outputs/opportunities.json", [o.dict() for o in opportunities])
    publish("outputs/workflow.json", workflow)
    return rules, opportunities, workflow
