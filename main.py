import json
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START

class GraphState(TypedDict):
    question: str
    generation: str                # retriever output (summary + json)
    parsed: dict                   # parsed retriever JSON (object)
    opportunities: list            # list of opportunity dicts
    selected_id: str               # "AUTO-001"
    selected_opportunity: dict     # chosen one
    n8n_workflow: dict             # final workflow JSON
    done: bool

def extract_first_json(text: str) -> dict:
    start = text.find("{")
    if start == -1:
        raise ValueError("No '{' found in text")
    
    # Extraction simplifiée mais robuste pour le test
    # On cherche la dernière accolade fermante
    end = text.rfind("}")
    if end == -1:
        raise ValueError("No '}' found in text")
        
    return json.loads(text[start:end+1])

def retriever_output(state: GraphState) -> GraphState:
    print("\n--- NODE: Retriever Output ---")
    gen = state["generation"]
    parsed = extract_first_json(gen)
    state["parsed"] = parsed
    state["opportunities"] = parsed.get("opportunities", [])
    return state

def human_select_opportunity(state: GraphState) -> GraphState:
    print("\n=== AUTOMATION OPPORTUNITIES ===")
    opps = state.get("opportunities", [])
    
    if not opps:
        print("No opportunities found.")
        state["done"] = True
        return state

    # Tri par priorité
    opps_sorted = sorted(opps, key=lambda x: int(x.get("priority_score", 0)), reverse=True)
    
    for i, opp in enumerate(opps_sorted, start=1):
        print(f"{i}) [{opp.get('id','?')}] {opp.get('title')} (Prio: {opp.get('priority_score')})")

    # ATTENTION: input() fonctionne ici si lancé dans un terminal standard
    choice = input("\nChoose a number (or 'q' to quit): ").strip().lower()

    if choice in ("quit", "q", "exit"):
        state["done"] = True
        return state

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(opps_sorted):
            selected = opps_sorted[idx]
            state["selected_id"] = selected.get("id", "")
            state["selected_opportunity"] = selected
            print(f"✅ Selection confirmed: {selected.get('title')}")
            return state

    print("Invalid choice, defaulting to first.")
    state["selected_opportunity"] = opps_sorted[0]
    return state

def planner_node(state: GraphState) -> GraphState:
    print("\n--- NODE: Planner (Preparing n8n Workflow) ---")
    opp = state["selected_opportunity"]
    
    # Ici, vous pourriez appeler votre LLM avec MCP pour générer le JSON
    # Pour l'exemple, nous créons une structure de base
    state["n8n_workflow"] = {
        "workflow_name": f"Workflow_{opp['id']}",
        "nodes": opp.get("steps_outline", []),
        "status": "ready_for_generation"
    }
    print(f"Workflow logic planned for {opp['id']}")
    return state

# Construction du Graphe
workflow = StateGraph(GraphState)

workflow.add_node("retriever_output", retriever_output)
workflow.add_node("human_select_opportunity", human_select_opportunity)
workflow.add_node("planner", planner_node)

workflow.add_edge(START, "retriever_output")
workflow.add_edge("retriever_output", "human_select_opportunity")
workflow.add_edge("human_select_opportunity", "planner")
workflow.add_edge("planner", END)

app = workflow.compile()

def main():
    test_json = """
    {
  "company_context": {
    "inferred_industries_or_functions": [
      "Enterprise Software",
      "Cloud Services"
    ],
    "tools_mentioned": [
      "Power Apps",
      "Power Automate",
      "Dataverse",
      "Microsoft Entra ID"
    ],
    "confidence": 1
  },
  "opportunities": [
    {
      "id": "AUTO-001",
      "department": "HR",
      "title": "Automated Access Removal on Employee Termination",
      "problem_statement": "Manual removal of user accounts after termination leads to security risks and orphaned accounts.",
      "current_process_summary": "HR notifies IT via email; process is manual and error-prone.",
      "automation_goal": "Automatically trigger deprovisioning upon termination record submission with an HR approval gate.",
      "classification": "EVIDENCED",
      "evidence_snippets": [
        {
          "source_type": "PDF",
          "source_ref": "Section 5 A.9 Access Control",
          "snippet": "Remove access to information systems upon termination."
        }
      ],
      "trigger": {
        "type": "form_submitted",
        "details": "Employee termination form submitted in HR system."
      },
      "inputs": ["Termination record ID", "Employee email", "Last role"],
      "outputs": ["Deprovisioning confirmation", "Audit log entry"],
      "integrations": ["Gmail/Outlook", "Local DB", "Slack", "Google Sheets"],
      "steps_outline": [
        "Receive termination form data",
        "Create Slack approval request for HR manager",
        "On approval: call identity database to disable accounts",
        "Send notification email to manager",
        "Write immutable audit entry to Google Sheets"
      ],
      "human_in_the_loop": {
        "required": true,
        "approval_reason": "Validate termination date and prevent accidental lockout",
        "approval_step": "Slack approval request"
      },
      "risk_notes": [
        "Exclude critical service accounts from automated deletion",
        "Ensure audit logs meet regulatory retention requirements"
      ],
      "impact_score": 5,
      "priority_score": 6
    },
    {
      "id": "2",
      "department": "IT",
      "title": "Automated Audit Log Generation for Access Changes",
      "problem_statement": "Permission changes are not consistently logged, failing compliance audits.",
      "current_process_summary": "Admins manually record changes in spreadsheets.",
      "automation_goal": "Capture all access control changes in real-time and append to a secure log.",
      "classification": "EVIDENCED",
      "trigger": {
        "type": "db_record_created",
        "details": "Trigger on database update in identity management system."
      },
      "steps_outline": [
        "Detect database change event",
        "Compose structured log entry",
        "Append to Google Sheet audit log",
        "Post summary to Teams/Slack compliance channel"
      ],
      "human_in_the_loop": { "required": false },
      "impact_score": 4,
      "priority_score": 5
    }
  ]
}
    """
    
    initial_state = {
        "generation": test_json,
        "done": False,
        "opportunities": [],
        "selected_opportunity": {}
    }

    # Utilisation de .invoke()
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL RESULT ---")
    if "n8n_workflow" in final_state:
        print(json.dumps(final_state["n8n_workflow"], indent=2))

if __name__ == "__main__":
    main()