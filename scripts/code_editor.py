from langchain_core.language_models.chat_models import BaseChatModel
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from tools.filesystem_tools import list_files, read_file, write_file
import os

def run_editing_agent(llm: BaseChatModel, instruction: str, project_path: str) -> dict:
    # IMPORTANT: Change the current working directory for the agent's tools
    # This is a security measure to contain the agent's actions.
    original_cwd = os.getcwd()
    try:
        os.chdir(project_path)
        
        tools = [list_files, read_file, write_file]
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        
        result = agent_executor.invoke({"input": instruction})
        
    finally:
        # Always change back to the original directory
        os.chdir(original_cwd)
        
    return result
