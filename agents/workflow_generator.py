"""Generate simple workflow from rules/opportunities."""

def generate_workflow(opportunities):
    # Very small stub that composes steps
    steps = []
    for i, o in enumerate(opportunities, start=1):
        steps.append({"step": i, "action": f"Review: {o.title}", "opportunity_id": o.id})
    return {"steps": steps}
