# services/planning_service.py
from pydantic import BaseModel
from typing import Optional
from langchain_core.output_parsers import StrOutputParser

from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task,
)

class PlanRequest(BaseModel):
    description: str

class PlanningService(AbstractTaskService):
    """Service responsible for the feature planning task."""
    def __init__(self, task_name: str = "planning"):
        self.task_name = task_name

    def execute(self, description: str, model_override: Optional[str] = None) -> dict:
        try:
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            prompt = get_prompt_template_for_task(self.task_name)
            
            chain = prompt | llm | StrOutputParser()
            plan = chain.invoke({"feature": description})

            return {"plan": plan, "model_used": f"{provider}:{model_name}"}
        except Exception as e:
            raise ServiceExecutionError(message=f"Error in PlanningService: {e}", original_exception=e)
