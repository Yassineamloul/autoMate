import json
import asyncio
import os
import httpx
import re
from typing import Any, Dict, List
from typing_extensions import TypedDict
from types import SimpleNamespace

# LangChain / LangGraph Imports
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END, StateGraph, START

# MCP Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv
load_dotenv()

# ---------------------------
# 0. Configuration & Sanitization
# ---------------------------
# Sanitize the URL to prevent 404 errors (removes /mcp-server/http if present)
RAW_N8N_URL = os.getenv("N8N_BASE_URL")
if not RAW_N8N_URL:
    raise ValueError("N8N_BASE_URL must be set in .env file")
N8N_BASE_URL = RAW_N8N_URL.split("/mcp-server")[0].strip("/")

# MCP Server Parameters
N8N_SERVER_PARAMS = StdioServerParameters(
    transport="stdio",
    command="npx",
    args=["-y", "mcp-n8n"],
    env={
        "N8N_BASE_URL": N8N_BASE_URL, # Uses the sanitized URL
        "N8N_API_KEY": os.getenv("N8N_API_KEY")
    }
)

CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY")

# ---------------------------
# 1. State Definition
# ---------------------------
class GraphState(TypedDict, total=False):
    generation: str                # Raw input JSON text
    parsed: Dict[str, Any]         # Parsed JSON
    opportunities: List[Dict[str, Any]]
    selected_id: str
    selected_opportunity: Dict[str, Any]
    n8n_workflow: Dict[str, Any]   # Generated technical plan
    done: bool

# ---------------------------
# 2. Helper Functions
# ---------------------------
async def call_n8n_mcp_tool(tool_name: str, arguments: dict):
    """Calls the actual n8n MCP server."""
    async with stdio_client(N8N_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result

async def call_context7_tool(tool_name: str, arguments: dict):
    """Helper function to call Context7 MCP API via HTTP."""
    endpoint = "https://mcp.context7.com/mcp"
    headers = {
        "Content-Type": "application/json",
        "CONTEXT7_API_KEY": CONTEXT7_API_KEY,
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
        "id": 1
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(endpoint, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            content_text = ""
            if "result" in data and "content" in data["result"]:
                for item in data["result"]["content"]:
                    if item.get("type") == "text":
                        content_text += item.get("text", "") + "\n"
            return SimpleNamespace(content=content_text)
        except Exception as e:
            print(f"❌ Context7 Call Error: {e}")
            return SimpleNamespace(content=f"Error retrieving docs: {str(e)}")

def extract_first_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No valid JSON found in text")
    return json.loads(text[start:end+1])

def clean_json_output(text: str) -> str:
    """Removes Markdown code blocks and whitespace."""
    text = text.strip()
    if "```" in text:
        text = text.split("```json")[-1].split("```")[0]
    return text.strip()

# ---------------------------
# 3. Nodes Implementation
# ---------------------------
async def retriever_output(state: GraphState) -> GraphState:
    print("\n--- NODE: Retriever Output ---")
    gen = state["generation"]
    parsed = extract_first_json(gen)
    state["parsed"] = parsed
    state["opportunities"] = parsed.get("opportunities", [])
    return state

async def human_select_opportunity(state: GraphState) -> GraphState:
    print("\n=== AUTOMATION OPPORTUNITIES ===")
    opps = state.get("opportunities", [])
    if not opps:
        state["done"] = True
        return state

    opps_sorted = sorted(opps, key=lambda x: int(x.get("priority_score", 0)), reverse=True)
    for i, opp in enumerate(opps_sorted, start=1):
        print(f"{i}) [{opp.get('id','?')}] {opp.get('title')} (Prio: {opp.get('priority_score')})")

    choice = input("\nChoose a number (or 'q' to quit): ").strip().lower()
    if choice in ("quit", "q", "exit"):
        state["done"] = True
        return state

    idx = int(choice) - 1 if choice.isdigit() else 0
    selected = opps_sorted[idx] if 0 <= idx < len(opps_sorted) else opps_sorted[0]
    
    state["selected_id"] = selected.get("id", "")
    state["selected_opportunity"] = selected
    print(f"✅ Selection confirmed: {selected.get('title')}")
    return state

async def planner_node(state: GraphState) -> GraphState:
    print("\n--- NODE: AI Planner (Smart Search & Context7) ---")
    opp = state["selected_opportunity"]
    
    # Increase timeout to prevent blocking on large models
    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.1, request_timeout=120.0)

    # STEP 1: Analysis
    analysis_prompt = f"""
    Analyze this automation opportunity: "{opp.get('title')}".
    Department: {opp.get('department')}
    Generate JSON with keywords (for search) and probable n8n nodes.
    Respond in JSON: {{ "keywords": [], "nodes": [] }}
    """
    analysis_res = llm.invoke([HumanMessage(content=analysis_prompt)])
    try:
        analysis = json.loads(clean_json_output(analysis_res.content))
    except:
        analysis = {"keywords": [opp.get('title').split()[0]], "nodes": []}
    
    print(f"🎯 Targeted Keywords: {analysis.get('keywords')}")

    # STEP 2: Template Search
    found_templates = []
    try:
        list_res = await call_n8n_mcp_tool("n8n_list_workflow_templates", {})
        all_templates = []
        if list_res and list_res.content:
            try:
                # Handle content being a list of text objects
                content_str = list_res.content[0].text if isinstance(list_res.content, list) else str(list_res.content)
                raw_data = json.loads(content_str)
                if isinstance(raw_data, dict) and "templates" in raw_data:
                    all_templates = raw_data["templates"]
                elif isinstance(raw_data, list):
                    all_templates = raw_data
            except: pass

        keywords = [k.lower() for k in analysis.get('keywords', [])]
        for t in all_templates:
            t_name = str(t.get('name', '')).lower()
            if any(k in t_name for k in keywords):
                found_templates.append({"id": t.get('id'), "name": t.get('name')})
        found_templates = found_templates[:5]
    except Exception as e:
        print(f"⚠️ Search Warning: {e}")

    templates_context = json.dumps(found_templates) if found_templates else "No matching templates found."

    # STEP 3: Documentation
    docs_context = ""
    try:
        if analysis.get('nodes'):
            query_doc = f"Configuration parameters for n8n nodes: {', '.join(analysis['nodes'][:5])}"
            c7_res = await call_context7_tool("query-docs", {"libraryId": "/n8n-io/n8n-docs", "query": query_doc})
            docs_context = c7_res.content
            print("📚 Context7 Documentation retrieved.")
    except Exception as e:
        print(f"⚠️ Context7 unavailable: {e}")

    # STEP 4: Planning
    print("🤖 Generating Strategy (This may take 30s)...")
    system_prompt = (
        "You are a Senior n8n Solutions Architect.\n"
        "DECISION MATRIX:\n"
        "1. USE TEMPLATE: If found templates match >50%, select it.\n"
        "2. BUILD CUSTOM: Otherwise, design a custom workflow.\n"
        "OUTPUT: Valid JSON only. No Markdown."
    )
    
    user_msg = f"""
    Opportunity: {opp.get('title')}
    Templates: {templates_context}
    Docs (Truncated): {docs_context[:1500]} 
    
    Generate JSON Plan:
    {{
      "strategy": "use_template" | "build_custom",
      "template_id": "ID or null",
      "implementation_plan": ["Step 1", "Step 2"],
      "required_nodes": ["Node 1"]
    }}
    """
    
    final_response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_msg)])
    clean_content = clean_json_output(final_response.content)

    try:
        plan_json = json.loads(clean_content)
    except json.JSONDecodeError:
        print("❌ JSON Parse Failed. Fallback to custom.")
        plan_json = {"strategy": "build_custom", "implementation_plan": ["Manual Build"], "required_nodes": []}

    state["n8n_workflow"] = plan_json
    print(f"✅ Decision taken: {plan_json.get('strategy')}")
    return state

async def executor_node(state: GraphState) -> GraphState:
    print("\n--- NODE: Executor (JSON Generator) ---")
    plan = state.get("n8n_workflow", {})
    strategy = plan.get("strategy")
    
    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0, request_timeout=120.0)
    workflow_name = f"Auto-Generated: {state['selected_opportunity'].get('title')}"

    # Helper: Clean LLM Output
    def clean_json_output(text):
        text = text.strip()
        if "```" in text:
            text = text.split("```json")[-1].split("```")[0]
        return text.strip()

    # ====================================================
    # CASE 1: USE EXISTING TEMPLATE
    # ====================================================
    if strategy == "use_template":
        template_id = plan.get("template_id")
        print(f"🚀 Strategy: Fetch Template JSON {template_id}")
        print(f"   👉 Download it here: [https://n8n.io/workflows/](https://n8n.io/workflows/){template_id}")

    # ====================================================
    # CASE 2: BUILD CUSTOM (Fixed Connections)
    # ====================================================
    if strategy == "build_custom":
        print("🛠️ Strategy: Build Custom JSON (Offline Mode)")
        required_nodes = plan.get("required_nodes", [])
        
        # 1. Fetch Schemas
        schemas = ""
        try:
            if required_nodes:
                q = f"JSON parameters for: {', '.join(required_nodes[:3])}"
                c7 = await call_context7_tool("query-docs", {"libraryId": "/n8n-io/n8n-docs", "query": q})
                schemas = c7.content
        except: pass

        # 2. Generate JSON (With STRICT Connection Rules)
        print("   🤖 Generating Workflow JSON...")
        
        # 👇 THIS IS THE CRITICAL FIX IN THE PROMPT 👇
        sys_prompt = (
            "You are an n8n Expert. Output valid JSON with 'nodes' (array) and 'connections' (object).\n"
            "CRITICAL CONNECTION RULES:\n"
            "1. The 'connections' object must use a DOUBLE ARRAY structure for every output.\n"
            "   WRONG: 'Node A': { 'main': [ { 'node': 'Node B', ... } ] }\n"
            "   RIGHT: 'Node A': { 'main': [ [ { 'node': 'Node B', 'type': 'main', 'index': 0 } ] ] }\n"
            "2. Note the extra brackets [ [ ... ] ]. This is mandatory for n8n to see the lines.\n"
            "3. Do not use Markdown."
        )
        
        usr_msg = f"Plan: {json.dumps(plan.get('implementation_plan'))}\nDocs: {schemas[:2000]}\nGenerate JSON:"
        
        res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=usr_msg)])
        clean_code = clean_json_output(res.content)
        
        try:
            # Validate JSON
            wf_json = json.loads(clean_code)
            
            # 3. SAVE TO FILE
            filename = f"workflow_{state['selected_id']}.json"
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(wf_json, f, indent=2)
                
            print(f"\n✅ SUCCESS! Workflow saved to: {filename}")
            print("   👇 COPY THIS JSON BELOW 👇")
            print("-" * 40)
            print(clean_code)
            print("-" * 40)

        except json.JSONDecodeError as e:
            print(f"   ❌ JSON Generation Error: {e}")
            print(f"   RAW: {clean_code[:100]}...")

    state["done"] = True
    return state
# ---------------------------
# 4. Graph Construction
# ---------------------------
def route_after_human(state: GraphState):
    if state.get("done"): return "end"
    return "continue"

workflow = StateGraph(GraphState)
workflow.add_node("retriever_output", retriever_output)
workflow.add_node("human_select", human_select_opportunity)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

workflow.add_edge(START, "retriever_output")
workflow.add_edge("retriever_output", "human_select")
workflow.add_conditional_edges("human_select", route_after_human, {"continue": "planner", "end": END})
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", END)

app = workflow.compile()

# ---------------------------
# 5. Main Execution
# ---------------------------
async def main():
    test_json = """ { "opportunities": [ { "id": "1", "department": "HR", "title": "Access Removal", "priority_score": 6 }, { "id": "2", "department": "Sales", "title": "Save Gmail Attachments to Google Drive", "priority_score": 5 },{ "id": "3", "department": "Finance", "title": "Sync new Stripe payments to Google Sheets", "priority_score": 7 }, { "id": "1", "department": "Marketing", "title": "Post Typeform submissions to Slack channel", "priority_score": 8 }, { "id": "2", "department": "IT", "title": "Create a simple Telegram bot that replies to messages", "priority_score": 6 }, { "id": "3", "department": "Research", "title": "Scrape a website daily and email me the text", "priority_score": 5 }] } """
    
    print("\n🚀 Starting Automation Agent...")
    print(f"🔧 Target n8n Instance: {N8N_BASE_URL}")
    
    initial_state = {"generation": test_json, "done": False}
    final_state = await app.ainvoke(initial_state)
    
    print("\n--- PROCESS COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(main())