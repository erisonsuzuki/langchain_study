# services/editing_service.py
from pydantic import BaseModel
from typing import Optional
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.settings import resolve_model_for_task, get_llm_settings_for_task, get_llm_instance
from tools.filesystem_tools import list_files, read_file, write_file

class EditRequest(BaseModel):
    instruction: str

class EditingService(AbstractTaskService):
    """Service that uses an autonomous agent to perform code edits."""
    def __init__(self, task_name: str = "editing"):
        self.task_name = task_name

    def execute(self, instruction: str, model_override: Optional[str] = None) -> dict:
        try:
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            tools = [list_files, read_file, write_file]
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
            
            # This is a long-running, synchronous task.
            result = agent_executor.invoke({"input": instruction})
            
            return {"agent_output": result, "model_used": f"{provider}:{model_name}"}
        except Exception as e:
            raise ServiceExecutionError(message=f"Error in EditingService: {e}", original_exception=e)
