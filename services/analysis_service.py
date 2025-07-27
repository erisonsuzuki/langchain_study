# services/analysis_service.py
from pydantic import BaseModel, Field
from typing import Optional
import os
from langchain_core.output_parsers import PydanticOutputParser

from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task,
)

# --- Pydantic Models ---
class AnalyzeRequest(BaseModel):
    file_path: str

class AnalysisResult(BaseModel):
    analysis_markdown: str = Field(description="A summary of the code analysis, formatted in Markdown.")
    passed: bool = Field(description="Whether the code passed the quality check.")

# --- Service Implementation ---
class AnalysisService(AbstractTaskService):
    def __init__(self, task_name: str = "analysis"):
        self.task_name = task_name

    def execute(self, file_path: str, model_override: Optional[str] = None) -> dict:
        try:
            language_map = {".py": "Python", ".rb": "Ruby", ".js": "JavaScript"}
            file_extension = os.path.splitext(file_path)[1]
            language = language_map.get(file_extension, "unknown")

            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()

            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            parser = PydanticOutputParser(pydantic_object=AnalysisResult)
            prompt = get_prompt_template_for_task(self.task_name)
            
            # The prompt now needs to be told how to determine the 'passed' boolean.
            # We'll add this instruction to the chain's input.
            chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

            analysis_result_object = chain.invoke({"language": language, "code": source_code})

            return {"analysis": analysis_result_object.dict(), "model_used": f"{provider}:{model_name}"}
        except FileNotFoundError:
             raise ServiceExecutionError(message=f"File not found at path: {file_path}")
        except Exception as e:
            raise ServiceExecutionError(message=f"Error in AnalysisService: {e}", original_exception=e)
