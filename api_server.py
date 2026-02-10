"""
FastAPI Server for AutoMate Studio
Connects the web UI to the Python graph.py workflow
"""
import os
import shutil
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import json

# Initialize FastAPI (lazy import graph to speed up startup)
api = FastAPI(title="AutoMate API", version="1.0.0")

# Enable CORS for frontend
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Store active sessions (in production, use Redis or database)
sessions: Dict[str, Dict[str, Any]] = {}


class OpportunitySelection(BaseModel):
    session_id: str
    opportunity_index: int


class WorkflowRequest(BaseModel):
    session_id: str


def clean_data_directory():
    """Remove all files from data directory"""
    import time
    max_retries = 3
    
    for item in DATA_DIR.iterdir():
        for attempt in range(max_retries):
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
                break  # Success, exit retry loop
            except (PermissionError, OSError) as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)  # Wait and retry
                else:
                    print(f"⚠️ Could not delete {item.name}: {e}")
                    # Continue anyway, don't fail the whole operation
    print("✅ Data directory cleaned")


def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """Save uploaded files to data directory"""
    saved_paths = []
    for file in files:
        file_path = DATA_DIR / file.filename
        try:
            with open(file_path, "wb") as f:
                content = file.file.read()
                f.write(content)
            # Ensure file handle is released
            file.file.close()
            saved_paths.append(str(file_path))
        except Exception as e:
            print(f"⚠️ Error saving {file.filename}: {e}")
    return saved_paths


async def run_rag_phase(question: str) -> Dict[str, Any]:
    """Run the RAG phase to find automation opportunities"""
    # Lazy import to speed up server startup
    from graph import GraphState, retrieve, grade_documents, decide_to_generate, transform_query, generate, grade_generation, parse_output
    from langgraph.graph import StateGraph, START, END
    
    # Build a minimal graph without human interaction
    workflow = StateGraph(GraphState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("generate", generate)
    workflow.add_node("parse_output", parse_output)
    
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        grade_generation,
        {"parse_output": "parse_output"}
    )
    workflow.add_edge("parse_output", END)
    
    app = workflow.compile()
    
    initial_state: GraphState = {
        "question": question,
        "generation": "",
        "documents": [],
        "retries": 0,
        "parsed_opportunities": {},
        "opportunities": [],
        "selected_id": "",
        "selected_opportunity": {},
        "n8n_workflow": {},
        "done": False
    }
    
    # Run graph until we get opportunities (before human_select)
    result = None
    async for output in app.astream(initial_state):
        result = output
        # Stop after parse_output node
        if "parse_output" in output:
            break
    
    if result and "parse_output" in result:
        state = result["parse_output"]
        return {
            "opportunities": state.get("opportunities", []),
            "state": state
        }
    
    return {"opportunities": [], "state": initial_state}


async def run_builder_phase(state, selected_index: int) -> Dict[str, Any]:
    """Run the builder phase with selected opportunity"""
    # Lazy import
    from graph import GraphState, planner_node, executor_node
    from langgraph.graph import StateGraph, START, END
    
    opportunities = state.get("opportunities", [])
    
    if not opportunities or selected_index >= len(opportunities):
        raise ValueError("Invalid opportunity selection")
    
    # Sort by priority
    opps_sorted = sorted(
        opportunities,
        key=lambda x: int(x.get("priority_score", 0)),
        reverse=True
    )
    selected = opps_sorted[selected_index]
    
    # Update state with selection
    state["selected_id"] = selected.get("id")
    state["selected_opportunity"] = selected
    state["done"] = False
    
    # Build a minimal graph for planner and executor only
    workflow = StateGraph(GraphState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)
    
    app = workflow.compile()
    
    # Continue the graph from planner
    result = None
    async for output in app.astream(state, {"recursion_limit": 50}):
        result = output
        if "executor" in output:
            break
    
    # Read the generated workflow file
    workflow_path = Path("workflow_final.json")
    if workflow_path.exists():
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)
        return {
            "success": True,
            "workflow": workflow_data,
            "selected_opportunity": selected
        }
    
    return {
        "success": False,
        "message": "Workflow generation failed"
    }


@api.get("/")
async def root():
    return {"message": "AutoMate API is running", "version": "1.0.0"}


@api.post("/api/analyze")
async def analyze_documents(
    files: List[UploadFile] = File(...),
    context_url: Optional[str] = Form(None),
    question: Optional[str] = Form(None)
):
    """
    Upload files and analyze them to find automation opportunities
    """
    print(f"\n{'='*60}")
    print(f"📥 ANALYZE REQUEST RECEIVED")
    print(f"Files: {[f.filename for f in files]}")
    print(f"Context URL: {context_url}")
    print(f"{'='*60}\n")
    
    try:
        # Clean previous files
        clean_data_directory()
        
        # Save new files
        saved_paths = save_uploaded_files(files)
        print(f"📁 Saved {len(saved_paths)} files to data directory")
        
        # Prepare question for RAG
        if not question:
            question = (
                "Analyze these documents and identify automation opportunities. "
                "What processes can be automated using n8n workflows?"
            )
        
        if context_url:
            question += f" Context URL: {context_url}"
        
        # Run RAG phase
        result = await run_rag_phase(question)
        
        # Create session
        import uuid
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "state": result["state"],
            "files": saved_paths,
            "question": question
        }
        
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "opportunities": result["opportunities"],
            "files_processed": len(saved_paths)
        })
        
    except Exception as e:
        print(f"❌ Error in analyze: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@api.post("/api/build-workflow")
async def build_workflow(selection: OpportunitySelection):
    """
    Build workflow for selected opportunity
    """
    try:
        session_id = selection.session_id
        
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        state = session_data["state"]
        
        # Run builder phase
        result = await run_builder_phase(state, selection.opportunity_index)
        
        if result["success"]:
            return JSONResponse({
                "success": True,
                "workflow": result["workflow"],
                "selected_opportunity": result["selected_opportunity"]
            })
        else:
            raise HTTPException(status_code=500, detail=result.get("message", "Build failed"))
            
    except Exception as e:
        print(f"❌ Error in build_workflow: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/api/download-workflow")
async def download_workflow():
    """
    Download the generated workflow JSON file
    """
    workflow_path = Path("workflow_final.json")
    if not workflow_path.exists():
        raise HTTPException(status_code=404, detail="Workflow file not found")
    
    return FileResponse(
        workflow_path,
        media_type="application/json",
        filename="workflow.json"
    )


@api.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "data_dir": str(DATA_DIR),
        "active_sessions": len(sessions)
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AutoMate API Server...")
    print("📡 Server will be available at http://localhost:8000")
    print("📖 API docs at http://localhost:8000/docs")
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")
