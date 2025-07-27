from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task
)

from scripts.task_planner import run_smart_feature_planning
from scripts.doc_generator import run_scalable_doc_generation
from scripts.code_analyzer import run_code_analysis
from scripts.code_editor import run_editing_agent

# --- Data Models for API Requests (Pydantic) ---
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
    project_path: str = "/app/workspace"

app = FastAPI(
    title="AI Developer Assistant (Final Version)",
    description="A provider-agnostic API to automate complex development tasks.",
    version="final"
)

async def _get_task_llm(task_name: str, model_override: Optional[str] = None):
    provider, model_name = resolve_model_for_task(task_name, model_override)
    llm_settings = get_llm_settings_for_task(task_name)
    llm = get_llm_instance(provider, model_name, llm_settings)
    return llm, f"{provider}:{model_name}"

@app.get("/", summary="Check server status")
def read_root():
    return {"status": "AI Assistant is online."}

@app.post("/plan-feature", summary="Create a smart, contextual plan for a new feature")
async def plan_feature_endpoint(request: PlanRequest):
    try:
        llm, model_used = await _get_task_llm("planning", request.model)
        prompt = get_prompt_template_for_task("planning_classifier")
        
        plan = run_smart_feature_planning(llm, prompt, request.description)
        
        return {"plan": plan, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-docs", summary="Generate scalable documentation for a project")
async def generate_docs_endpoint(request: DocsRequest):
    try:
        llm, model_used = await _get_task_llm("documentation", request.model)
        docs_content = run_scalable_doc_generation(llm, request.project_path)
        return {"docs_generated": docs_content, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-code", summary="Analyze a code file for best practices")
async def analyze_code_endpoint(request: AnalyzeRequest):
    try:
        llm, model_used = await _get_task_llm("analysis", request.model)
        prompt = get_prompt_template_for_task("analysis")
        analysis_result, analysis_passed = run_code_analysis(llm, prompt, request.file_path)
        return {"analysis": analysis_result, "passed": analysis_passed, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/edit-code-agent", summary="Run an autonomous agent to edit code")
async def edit_code_agent_endpoint(request: EditRequest):
    try:
        llm, model_used = await _get_task_llm("editing", request.model)
        result = run_editing_agent(llm, request.instruction, request.project_path)
        return {"agent_output": result, "model_used": model_used}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
