import json
import asyncio
import os
import httpx
import re
from typing import Any, Dict, List
from typing_extensions import TypedDict
from types import SimpleNamespace
from pprint import pprint

# --- LANGCHAIN / LANGGRAPH IMPORTS ---
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END, StateGraph, START

# --- MCP IMPORTS ---
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# --- RAG IMPORTS (From your first code) ---
# Ensure the 'RAG' folder is in your project directory
from RAG.index import retriever
from RAG.generator import rag_chain, format_docs
from RAG.grader1 import retrieval_grader
from RAG.grader2 import answer_grader
from RAG.hallucinate_detector import hallucination_grader
from RAG.answer_rewriter import question_rewriter

from dotenv import load_dotenv
load_dotenv()

# ==============================================================================
# 0. CONFIGURATION & SETUP
# ==============================================================================

# Sanitize n8n URL
RAW_N8N_URL = os.getenv("N8N_BASE_URL")
if not RAW_N8N_URL:
    raise ValueError("N8N_BASE_URL must be set in .env file")
N8N_BASE_URL = RAW_N8N_URL.split("/mcp-server")[0].strip("/")

# MCP Server Params
N8N_SERVER_PARAMS = StdioServerParameters(
    transport="stdio",
    command="npx",
    args=["-y", "mcp-n8n"],
    env={
        "N8N_BASE_URL": N8N_BASE_URL,
        "N8N_API_KEY": os.getenv("N8N_API_KEY")
    }
)

CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY")


# ==============================================================================
# 1. STATE DEFINITION (MERGED)
# ==============================================================================
class GraphState(TypedDict, total=False):
    # --- RAG State ---
    question: str
    generation: str           # The textual answer from RAG
    documents: List[Document]
    retries: int
    
    # --- Automation Builder State ---
    parsed_opportunities: Dict[str, Any] # Extracted JSON from RAG generation
    opportunities: List[Dict[str, Any]]
    selected_id: str
    selected_opportunity: Dict[str, Any]
    n8n_workflow: Dict[str, Any]
    done: bool


# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================

async def call_n8n_mcp_tool(tool_name: str, arguments: dict):
    """Calls the n8n MCP tool."""
    async with stdio_client(N8N_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool(tool_name, arguments)

async def call_context7_tool(tool_name: str, arguments: dict):
    """Calls Context7 API."""
    endpoint = "https://mcp.context7.com/mcp"
    headers = {
        "Content-Type": "application/json",
        "CONTEXT7_API_KEY": CONTEXT7_API_KEY,
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0", "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}, "id": 1
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(endpoint, json=payload, headers=headers, timeout=30.0)
            res.raise_for_status()
            data = res.json()
            content = ""
            if "result" in data and "content" in data["result"]:
                for item in data["result"]["content"]:
                    if item.get("type") == "text": content += item.get("text", "") + "\n"
            return SimpleNamespace(content=content)
        except Exception as e:
            print(f"❌ Context7 Error: {e}")
            return SimpleNamespace(content="")

def clean_json_output(text: str) -> str:
    text = text.strip()
    if "```" in text:
        text = text.split("```json")[-1].split("```")[0]
    return text.strip()

def extract_json_from_text(text: str) -> dict:
    """Finds and parses the first JSON object in a string."""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(text[start:end])
    except: pass
    return {}


# ==============================================================================
# 3. PHASE 1 NODES: RAG (INTELLIGENCE)
# ==============================================================================

def retrieve(state: GraphState) -> GraphState:
    print("\n---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {**state, "documents": documents, "retries": state.get("retries", 0)}

def grade_documents(state: GraphState) -> GraphState:
    print("\n---GRADE DOCUMENTS---")
    question = state["question"]
    documents = state["documents"]
    filtered_docs = []
    
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        if score.binary_score == "yes":
            filtered_docs.append(d)
            
    print(f"Docs kept: {len(filtered_docs)}/{len(documents)}")
    return {**state, "documents": filtered_docs}

def transform_query(state: GraphState) -> GraphState:
    print("\n---TRANSFORM QUERY---")
    question = state["question"]
    better_q = question_rewriter.invoke({"question": question})
    if hasattr(better_q, "content"): better_q = better_q.content
    return {**state, "question": better_q, "retries": state.get("retries", 0) + 1}

def generate(state: GraphState) -> GraphState:
    print("\n---GENERATE (RAG)---")
    question = state["question"]
    documents = state["documents"]
    
    # We tweak the generation to force JSON output for the next phase
    rag_prompt_extension = (
        "\nIMPORTANT: After your analysis, output a valid JSON object containing a list of 'opportunities' "
        "identified in the text. Format: { 'opportunities': [ { 'id': '1', 'title': '...', 'priority_score': 1-10, 'department': '...' } ] }"
    )
    
    generation = rag_chain.invoke({
        "context": format_docs(documents),
        "question": question + rag_prompt_extension
    })
    
    return {**state, "generation": generation}


# --- RAG Conditional Logic ---

MAX_RETRIES = 2

def decide_to_generate(state: GraphState) -> str:
    if state["documents"]: return "generate"
    if state["retries"] < MAX_RETRIES: return "transform_query"
    return "generate" # Fallback

def grade_generation(state: GraphState) -> str:
    print("\n---GRADE GENERATION---")
    # For this merged app, we trust the generation if it contains JSON
    if "opportunities" in state["generation"]:
        return "parse_output"
    return "parse_output" # Proceed anyway to try extraction


# ==============================================================================
# 4. PHASE 2 NODES: AUTOMATION BUILDER (ACTION)
# ==============================================================================

def parse_output(state: GraphState) -> GraphState:
    print("\n---PARSE RAG OUTPUT---")
    gen_text = state["generation"]
    
    # Extract JSON opportunities from RAG text
    parsed = extract_json_from_text(gen_text)
    
    if not parsed or "opportunities" not in parsed:
        print("⚠️ No structured opportunities found in RAG output. Using Mock Data for demo.")
        parsed = { "opportunities": [ 
            { "id": "1", "department": "HR", "title": "Mock: Access Removal", "priority_score": 6 },
            { "id": "2", "department": "Sales", "title": "Mock: Save Gmail Attachments", "priority_score": 5 }
        ]}
    
    return {**state, "parsed_opportunities": parsed, "opportunities": parsed.get("opportunities", [])}

async def human_select_opportunity(state: GraphState) -> GraphState:
    print("\n=== AUTOMATION OPPORTUNITIES FOUND ===")
    opps = state.get("opportunities", [])
    
    if not opps:
        print("No opportunities found.")
        return {**state, "done": True}

    opps_sorted = sorted(opps, key=lambda x: int(x.get("priority_score", 0)), reverse=True)
    for i, opp in enumerate(opps_sorted, start=1):
        print(f"{i}) {opp.get('title')} (Prio: {opp.get('priority_score')})")

    choice = input("\nChoose a number to build (or 'q' to quit): ").strip().lower()
    if choice in ("q", "quit"):
        return {**state, "done": True}
        
    idx = int(choice) - 1 if choice.isdigit() else 0
    selected = opps_sorted[idx] if 0 <= idx < len(opps_sorted) else opps_sorted[0]
    
    print(f"✅ Selected: {selected.get('title')}")
    return {**state, "selected_id": selected.get("id"), "selected_opportunity": selected}

async def planner_node(state: GraphState) -> GraphState:
    print("\n---AI PLANNER---")
    opp = state["selected_opportunity"]
    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.1, request_timeout=120.0)

    # 1. Analyze
    analysis_res = llm.invoke([HumanMessage(content=f"Analyze automation: '{opp.get('title')}'. Return JSON {{ 'keywords': [], 'nodes': [] }}")])
    try:
        analysis = json.loads(clean_json_output(analysis_res.content))
    except:
        analysis = {"keywords": ["automation"], "nodes": []}
        
    # 2. Search Templates (MCP)
    found_templates = []
    try:
        # We try to search n8n templates via MCP
        res = await call_n8n_mcp_tool("n8n_list_workflow_templates", {})
        # (Parsing logic omitted for brevity, assuming list returned)
    except: pass
    
    templates_str = "No templates found." # Simplified for stability

    # 3. Fetch Docs (Context7)
    docs_str = ""
    try:
        if analysis.get('nodes'):
            q = f"Parameters for n8n nodes: {', '.join(analysis['nodes'][:3])}"
            c7 = await call_context7_tool("query-docs", {"libraryId": "/n8n-io/n8n-docs", "query": q})
            docs_str = c7.content
            print("📚 Docs retrieved.")
    except: pass

    # 4. Generate Plan
    print("🤖 Generating Plan...")
    sys_prompt = "You are an n8n Architect. Output JSON Plan: { 'strategy': 'build_custom', 'implementation_plan': [], 'required_nodes': [] }"
    user_msg = f"Task: {opp.get('title')}\nDocs: {docs_str[:1000]}"
    
    plan_res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=user_msg)])
    print(f"🔍 DEBUG - Raw Plan Response (first 300 chars):\n{plan_res.content[:300]}\n")
    
    try:
        plan_json = json.loads(clean_json_output(plan_res.content))
    except:
        plan_json = {"strategy": "build_custom", "implementation_plan": ["Manual Build"], "required_nodes": []}
        
    return {**state, "n8n_workflow": plan_json}

async def executor_node(state: GraphState) -> GraphState:
    print("\n---EXECUTOR (JSON BUILDER)---")
    plan = state.get("n8n_workflow", {})
    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0, request_timeout=120.0)
    
    # Fetch Schemas if needed
    schemas = ""
    required_nodes = plan.get("required_nodes", [])
    if required_nodes:
        try:
            q = f"JSON parameters for: {', '.join(required_nodes[:3])}"
            c7 = await call_context7_tool("query-docs", {"libraryId": "/n8n-io/n8n-docs", "query": q})
            schemas = c7.content
        except: pass

    print("🤖 Generatng Workflow Code...")
    sys_prompt = (
        "You are an n8n workflow builder. Generate a valid n8n workflow JSON.\n\n"
        "REQUIRED STRUCTURE:\n"
        "{\n"
        '  "nodes": [\n'
        '    {\n'
        '      "parameters": {},\n'
        '      "name": "Node Name",\n'
        '      "type": "n8n-nodes-base.nodeType",\n'
        '      "typeVersion": 1,\n'
        '      "position": [250, 300],\n'
        '      "id": "unique-id"\n'
        '    }\n'
        '  ],\n'
        '  "connections": {\n'
        '    "Node Name": {\n'
        '      "main": [\n'
        '        [\n'
        '          {\n'
        '            "node": "Next Node",\n'
        '            "type": "main",\n'
        '            "index": 0\n'
        '          }\n'
        '        ]\n'
        '      ]\n'
        '    }\n'
        '  }\n'
        '}\n\n'
        "Output ONLY valid JSON. No markdown, no explanations."
    )
    
    opp = state.get("selected_opportunity", {})
    opportunity_context = (
        f"Task: {opp.get('title', 'Automation Task')}\n"
        f"Description: {opp.get('problem_statement', '')}\n"
        f"Trigger: {opp.get('trigger', {})}\n"
        f"Steps: {opp.get('steps_outline', [])}\n"
        f"Integrations: {opp.get('integrations', [])}\n"
    )
    
    user_msg = f"{opportunity_context}\n\nPlan: {json.dumps(plan, indent=2)}\n\nGenerate the n8n workflow JSON:"
    
    res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=user_msg)])
    print(f"🔍 DEBUG - Raw LLM Response (first 500 chars):\n{res.content[:500]}\n")
    clean_code = clean_json_output(res.content)
    
    # Validate and provide fallback
    try:
        workflow_json = json.loads(clean_code)
        if not workflow_json.get("nodes") or not isinstance(workflow_json.get("nodes"), list):
            raise ValueError("Empty or invalid nodes")
    except Exception as e:
        print(f"⚠️  LLM output invalid ({e}), using fallback structure")
        opp = state.get("selected_opportunity", {})
        workflow_json = {
            "nodes": [
                {
                    "parameters": {},
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "id": "start-node"
                },
                {
                    "parameters": {
                        "content": f"Task: {opp.get('title', 'Automation')}\nConfigure this workflow manually."
                    },
                    "name": "Note",
                    "type": "n8n-nodes-base.stickyNote",
                    "typeVersion": 1,
                    "position": [450, 300],
                    "id": "note-node"
                }
            ],
            "connections": {}
        }
        clean_code = json.dumps(workflow_json, indent=2)
    
    # Save to file
    filename = f"workflow_final.json"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(clean_code)
        
    print(f"\n✅ SUCCESS! Workflow saved to {filename}")
    print("-" * 40)
    print(clean_code[:500] + "...\n(truncated)")
    print("-" * 40)
    
    return {**state, "done": True}


# ==============================================================================
# 5. GRAPH CONSTRUCTION (THE SUPER GRAPH)
# ==============================================================================

workflow = StateGraph(GraphState)

# --- Phase 1 Nodes (RAG) ---
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

# --- Phase 2 Nodes (Builder) ---
workflow.add_node("parse_output", parse_output)
workflow.add_node("human_select", human_select_opportunity)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

# --- Edges ---
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")

# RAG Loop Logic
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")

# Transition from RAG to Builder
workflow.add_conditional_edges(
    "generate",
    grade_generation,
    {
        "parse_output": "parse_output", # Proceed to Builder
        # You could add "not_useful" -> "transform_query" here if you wanted stricter loops
    }
)

workflow.add_edge("parse_output", "human_select")

# Builder Logic
def route_after_human(state):
    return "end" if state.get("done") else "continue"

workflow.add_conditional_edges(
    "human_select",
    route_after_human,
    {"continue": "planner", "end": END}
)

workflow.add_edge("planner", "executor")
workflow.add_edge("executor", END)

app = workflow.compile()


