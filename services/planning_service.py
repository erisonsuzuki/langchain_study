# services/planning_service.py
from pydantic import BaseModel
from typing import Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough

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
    """
    An advanced service that uses RunnableBranch to provide context-aware feature plans.
    """
    def __init__(self, task_name: str = "planning"):
        self.task_name = task_name

    def execute(self, description: str, model_override: Optional[str] = None) -> dict:
        try:
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            classifier_chain = (
                get_prompt_template_for_task("planning_classifier")
                | llm
                | StrOutputParser()
            )
            
            backend_chain = (
                get_prompt_template_for_task("planning_backend")
                | llm
                | StrOutputParser()
            )
            
            frontend_chain = (
                get_prompt_template_for_task("planning_frontend")
                | llm
                | StrOutputParser()
            )

            def route(input_data):
                classification = input_data["classification"]
                if "backend" in classification.lower():
                    print("INFO: Routing to BACKEND planner.")
                    return backend_chain
                elif "frontend" in classification.lower():
                    print("INFO: Routing to FRONTEND planner.")
                    return frontend_chain
                else:
                    print("INFO: Routing to default (BACKEND) planner.")
                    return backend_chain # Fallback

            full_chain = (
                RunnablePassthrough.assign(
                    classification=({"feature": lambda x: x["feature"]} | classifier_chain)
                )
                | RunnableLambda(route)
            )

            print(f"INFO: Running smart planner for feature: '{description}'")
            plan = full_chain.invoke({"feature": description})
            
            return {"plan": {"plan_markdown": plan}, "model_used": f"{provider}:{model_name}"}

        except Exception as e:
            raise ServiceExecutionError(message=f"Error in PlanningService: {e}", original_exception=e)
