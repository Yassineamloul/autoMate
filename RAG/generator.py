from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

def escape_braces(text: str) -> str:
    return text.replace("{", "{{").replace("}", "}}")

JSON_SCHEMA = """{
  "company_context": {
    "inferred_industries_or_functions": ["string"],
    "tools_mentioned": ["string"],
    "confidence": 1
  },
  "opportunities": [
    {
      "id": "1",
      "department": "Finance",
      "title": "string",
      "problem_statement": "string",
      "current_process_summary": "string",
      "automation_goal": "string",
      "classification": "EVIDENCED",
      "evidence_snippets": [
        {"source_type": "PDF", "source_ref": "string", "snippet": "string"}
      ],
      "trigger": {
        "type": "email_received",
        "details": "string"
      },
      "inputs": ["string"],
      "outputs": ["string"],
      "integrations": ["Gmail/Outlook"],
      "steps_outline": ["string"],
      "human_in_the_loop": {"required": true, "approval_reason": "string", "approval_step": "string"},
      "risk_notes": ["string"],
      "impact_score": 1,
      "time_saving_score": 1,
      "effort_score": 1,
      "priority_score": 1
    }
  ]
}"""


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

ULTRA_PROMPT = rf"""
You are an expert Prompt Engineer and AI Automation Architect acting as a “Retriever Agent” in an agentic workflow.

MISSION
Analyze the provided company documents (PDF text + URL content already retrieved) to identify high-impact automation opportunities. Your output will be consumed by a Planner Agent that generates n8n workflows.

SCOPE
- Document types: PDFs and URLs (policies, SOPs, emails/templates, process descriptions, checklists, onboarding docs, finance ops notes, support procedures, sales playbooks, etc.).
- Departments: Finance, Sales, HR, Operations, Customer Support, IT, Marketing—ALL.
- Automation stack assumptions: Gmail/Outlook, Slack/Teams, Google Sheets/Excel, Local Database, plus generic Webhooks/HTTP.
- Workflow complexity target: MEDIUM (conditions, branching, basic retries, logging, human approvals).

NON-NEGOTIABLE CONSTRAINTS
1) Evidence-first: Extract what the docs explicitly say. Include evidence snippets.
2) Suggestion mode allowed: If docs are incomplete, propose best-practice automations but label them SUGGESTED.
3) No hallucinated facts: Do not invent company-specific tools/policies/numbers. Use "unknown" if needed.
4) Safety guardrails:
   - Payments/refunds/transfers MUST require HUMAN APPROVAL before execution.
   - Avoid sending external emails automatically unless explicitly indicated; otherwise "draft + approval".
   - Never output secrets.
5) Output must be n8n-ready: triggers, inputs, outputs, steps, integrations, approvals.

HARD OUTPUT RULES (STRICT – NO EXCEPTIONS)
- Output MUST be a SINGLE valid JSON object.
- DO NOT output markdown.
- DO NOT use code fences (```).
- DO NOT add notes, explanations, headings, or commentary.
- DO NOT include text before or after the JSON.
- Any violation makes the output INVALID.

ENUM & VALUE CONSTRAINTS
- department MUST be exactly one of:
  Finance, Sales, HR, Operations, Support, IT, Marketing, Cross-functional
- classification MUST be exactly:
  EVIDENCED or SUGGESTED
- trigger.type MUST be exactly one of:
  email_received, form_submitted, sheet_row_added, db_record_created, schedule, manual
- integrations MUST ONLY include:
  Gmail/Outlook, Slack/Teams, Google Sheets/Excel, Local DB, HTTP/Webhook

SCORING RULES (MANDATORY)
- impact_score MUST be an integer between 1 and 5.
- time_saving_score MUST be an integer between 1 and 5.
- effort_score MUST be an integer between 1 and 5.
- priority_score MUST be an INTEGER.
- priority_score MUST equal:
  (impact_score + time_saving_score) - effort_score
- DO NOT write formulas. DO NOT write expressions. ONLY numbers.

OUTPUT FORMAT
- Output ONLY the JSON object.
- The JSON MUST match the schema EXACTLY.
- No extra keys. No missing keys.

JSON OUTPUT SCHEMA (STRICT)
{escape_braces(JSON_SCHEMA)}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", ULTRA_PROMPT),
    ("human",
     "Company documents (context):\n{context}\n\n"
     "Task:\n{question}\n\n"
     "Return:\n1) Short summary (max ~8 lines)\n2) STRICT JSON that matches the schema exactly.")
])

rag_chain = prompt | llm | StrOutputParser()



if __name__ == "__main__":
    # Optional local test (won't run on import)
    from .index import retriever  # local import to avoid circular imports in production

    q = "Analyze the documents and extract automation opportunities across departments. Output summary + JSON schema."
    docs = retriever.invoke(q)
    ans = rag_chain.invoke({"context": format_docs(docs), "question": q})
    print(ans)
