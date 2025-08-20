from pydantic import BaseModel
from typing import Optional, Dict, Any
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.prompt_loader import get_prompt_template_for_task
from config.llm_providers import get_llm_instance
from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
)
# Import the tools the agent can use from our tools module
from tools.filesystem_tools import list_files, read_file, write_file


class EditRequest(BaseModel):
    instruction: str


class EditingService(AbstractTaskService):
    """
    Service that uses an autonomous agent with filesystem tools to perform code edits.
    """
    def __init__(self, task_name: str = "editing"):
        self.task_name = task_name

    def execute(self, instruction: str, model_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes the code editing agent.

        Args:
            instruction: The high-level instruction for the agent to follow.
            model_override: Optional model identifier to override the default.

        Returns:
            A dictionary containing the agent's full output.
        """
        try:
            # 1. Resolve the model and its settings using our config system
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            # 2. Define the list of tools available to the agent
            tools = [list_files, read_file, write_file]
            
            # 3. Get the agent's core prompt from our local prompt file
            prompt = get_prompt_template_for_task("editing_agent")

            # 4. Create the ReAct (Reasoning and Acting) agent
            # This binds the LLM, tools, and prompt together
            agent = create_react_agent(llm, tools, prompt)

            # 5. Create the Agent Executor, which runs the agent's reasoning loop
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,  # Set to True to see the agent's thoughts in the server logs
                handle_parsing_errors=True,
                max_iterations=15 # Add a safety limit to prevent infinite loops
            )
            
            # 6. Invoke the agent with the user's instruction
            # NOTE: This is a potentially long-running, synchronous task. In a real production system,
            # this would ideally be handled by a background worker (e.g., Celery).
            print(f"INFO: Starting agent execution for instruction: '{instruction}'")
            result = agent_executor.invoke({"input": instruction})
            print("INFO: Agent execution finished.")
            
            return {"agent_output": result, "model_used": f"{provider}:{model_name}"}
            
        except Exception as e:
            # Wrap any potential error in our custom exception for clean API responses
            raise ServiceExecutionError(message=f"Error during agent execution in EditingService: {e}", original_exception=e)
