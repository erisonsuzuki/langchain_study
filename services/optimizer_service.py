# services/optimizer_service.py
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

class OptimizerRequest(BaseModel):
    raw_prompt: str

class OptimizerService(AbstractTaskService):
    """Service to refine and improve a user's raw prompt."""
    def __init__(self, task_name: str = "optimizer"):
        self.task_name = task_name

    def execute(self, raw_prompt: str, model_override: Optional[str] = None) -> dict:
        try:
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            prompt = get_prompt_template_for_task(self.task_name)
            
            # This is a straightforward text-generation task, so a simple chain is perfect.
            chain = prompt | llm | StrOutputParser()
            
            optimized_prompt = chain.invoke({"raw_prompt": raw_prompt})

            return {"optimized_prompt": optimized_prompt, "model_used": f"{provider}:{model_name}"}
        except Exception as e:
            raise ServiceExecutionError(message=f"Error in OptimizerService: {e}", original_exception=e)
