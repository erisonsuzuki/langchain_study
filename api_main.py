# api_main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task
)
from scripts.task_planner import run_feature_planning
from scripts.doc_generator import run_doc_generation
from scripts.code_analyzer import run_code_analysis
from scripts.code_editor import run_code_editing

# --- Data Models for Requests ---
class BaseRequest(BaseModel):
    model: Optional[str] = None # e.g., "OPENAI:gpt-4o"

class PlanRequest(BaseRequest):
    description: str

class DocsRequest(BaseRequest):
    project_path: str

class AnalyzeRequest(BaseRequest):
    file_path: str

class EditRequest(BaseRequest):
    instruction: str

app = FastAPI(
    title="AI Development Assistant (Final Version)",
    description="A provider-agnostic API to automate development tasks.",
    version="final"
)

@app.get("/", summary="Check server status")
def read_root():
    return {"status": "AI Assistant is online."}

async def _get_task_llm(task_name: str, model_override: Optional[str] = None):
    """Helper to resolve and instantiate the LLM for a task."""
    provider, model_name = resolve_model_for_task(task_name, model_override)
    llm_settings = get_llm_settings_for_task(task_name)
    llm = get_llm_instance(provider, model_name, llm_settings)
    return llm, f"{provider}:{model_name}"

@app.post("/plan-feature", summary="Create a technical plan for a new feature")
async def plan_feature_endpoint(request: PlanRequest):
    try:
        task_name = "planning"
        llm, model_used = await _get_task_llm(task_name, request.model)
        prompt = get_prompt_template_for_task(task_name)
        
        plan = run_feature_planning(llm, prompt, request.description)
        
        return {"plan": plan, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-docs", summary="Generate documentation for a project")
async def generate_docs_endpoint(request: DocsRequest):
    try:
        task_name = "documentation"
        llm, model_used = await _get_task_llm(task_name, request.model)
        prompt = get_prompt_template_for_task(task_name)
        
        docs_content = run_doc_generation(llm, prompt, request.project_path)

        return {"docs_generated": docs_content, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... Implement other endpoints for 'analysis' and 'editing' following the same pattern ...
