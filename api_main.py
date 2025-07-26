import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import the logic for each task
from scripts.task_planner import run_feature_planning
from scripts.doc_generator import run_doc_generation
from scripts.code_analyzer import run_code_analysis
from scripts.code_editor import run_code_editing

# --- Data Models for Requests (Pydantic) ---
class BaseRequest(BaseModel):
    model: str = "llama3:8b"

class PlanRequest(BaseRequest):
    description: str

class DocsRequest(BaseRequest):
    project_path: str

class AnalyzeRequest(BaseRequest):
    file_path: str
    
class EditRequest(BaseRequest):
    instruction: str
    # In a real scenario, you might also pass file contents or paths
    # For simplicity, we'll just pass the instruction.

# --- FastAPI Application Instance ---
app = FastAPI(
    title="AI Development Assistant",
    description="An API to automate development tasks using local LLMs.",
    version="5.0"
)

# Get the Ollama base URL from the environment, essential for Docker
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# --- API Endpoints ---

@app.get("/", summary="Check the server status")
def read_root():
    return {"status": "AI Assistant is online and ready for use."}

@app.post("/plan-feature", summary="Create a technical plan for a new feature")
async def plan_feature_endpoint(request: PlanRequest):
    try:
        plan = run_feature_planning(request.description, request.model, OLLAMA_BASE_URL)
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-docs", summary="Generate documentation (README) for a project")
async def generate_docs_endpoint(request: DocsRequest):
    try:
        # In Docker, the project path is what was mounted in the volume.
        # The API expects the path INSIDE the container.
        docs_content = run_doc_generation(request.project_path, request.model, OLLAMA_BASE_URL)
        return {"docs_generated": docs_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-code", summary="Analyze a code file for best practices")
async def analyze_code_endpoint(request: AnalyzeRequest):
    try:
        analysis_result, analysis_passed = run_code_analysis(request.file_path, request.model, OLLAMA_BASE_URL)
        return {"analysis": analysis_result, "passed": analysis_passed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/edit-code-plan", summary="Generate a plan to edit code based on an instruction")
async def edit_code_plan_endpoint(request: EditRequest):
    try:
        edit_plan = run_code_editing(request.instruction, request.model, OLLAMA_BASE_URL)
        return {"edit_plan": edit_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
