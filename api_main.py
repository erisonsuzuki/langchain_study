# api_main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Dict, Any

from core.exceptions import ServiceExecutionError

# --- Task Registry ---
from services.planning_service import PlanningService, PlanRequest
from services.docs_service import DocsService, DocsRequest
from services.analysis_service import AnalysisService, AnalyzeRequest
from services.editing_service import EditingService, EditRequest
from services.optimizer_service import OptimizerService, OptimizerRequest 

TASK_REGISTRY = {
    "planning": (PlanningService, PlanRequest),
    "documentation": (DocsService, DocsRequest),
    "analysis": (AnalysisService, AnalyzeRequest),
    "editing": (EditingService, EditRequest),
    "optimizer": (OptimizerService, OptimizerRequest),
}

# --- Generic Request Models ---
class GenericTaskRequest(BaseModel):
    model: str | None = None
    data: Dict[str, Any]

# --- FastAPI App Instance and Handlers ---
app = FastAPI(
    title="Generic AI Task Assistant (SOLID)",
    version="10.0"
)

@app.exception_handler(ServiceExecutionError)
async def service_exception_handler(request: Request, exc: ServiceExecutionError):
    return JSONResponse(
        status_code=500,
        content={"error": "An internal error occurred during task execution.", "detail": exc.message},
    )

@app.post("/tasks/{task_name}", summary="Executes any registered AI task", tags=["Tasks"])
async def execute_task(task_name: str, request: GenericTaskRequest):
    if task_name not in TASK_REGISTRY:
        return JSONResponse(status_code=404, content={"error": f"Task '{task_name}' not found."})

    ServiceClass, RequestModel = TASK_REGISTRY[task_name]
    try:
        task_data = RequestModel(**request.data)
    except ValidationError as e:
        return JSONResponse(status_code=422, content={"error": "Invalid data for the specified task.", "detail": str(e)})

    service_instance = ServiceClass(task_name)
    result = service_instance.execute(model_override=request.model, **task_data.model_dump())
    return result
