# services/docs_service.py
from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
# ... other imports
from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task,
)
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# --- Pydantic Models ---
class DocsRequest(BaseModel):
    project_path: str

class DocsResult(BaseModel):
    documentation_markdown: str = Field(description="The full README.md content as a Markdown string.")

# --- Service Implementation ---
class DocsService(AbstractTaskService):
    def __init__(self, task_name: str = "documentation"):
        self.task_name = task_name

    def execute(self, project_path: str, model_override: Optional[str] = None) -> dict:
        try:
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)
            
            # 2. Load documents with the intelligent loader 
            docs = self._load_documents(project_path)
            if not docs:
                return {"documentation": {"documentation_markdown": "No relevant source code files found."}, "model_used": f"{provider}:{model_name}"}

            # Map step remains a simple string output
            map_prompt = get_prompt_template_for_task("documentation_map")
            map_chain = map_prompt | llm | StrOutputParser()
            summaries = map_chain.batch([{"page_content": doc.page_content} for doc in docs])
            combined_summaries = "\n\n---\n\n".join(summaries)

            # Reduce step now uses the Pydantic parser
            parser = PydanticOutputParser(pydantic_object=DocsResult)
            reduce_prompt = get_prompt_template_for_task("documentation_reduce")
            reduce_chain = reduce_prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser

            final_result_object = reduce_chain.invoke({"doc_summaries": combined_summaries})
            
            return {"documentation": final_result_object.dict(), "model_used": f"{provider}:{model_name}"}
        except Exception as e:
            raise ServiceExecutionError(message=f"Error in DocsService: {e}", original_exception=e)

    def _load_documents(self, project_path: str) -> List[Document]:
        glob_patterns = ["**/*.py", "**/*.js", "**/*.ts", "**/*.rb", "**/*.go", "**/*.md"]
        exclude_patterns = ["**/__pycache__/**", "**/.git/**", "**/venv/**"]
        
        print(f"INFO: Scanning '{project_path}' for source files...")
        docs: List[Document] = []
        for pattern in glob_patterns:
            loader = DirectoryLoader(
                project_path,
                glob=pattern,
                exclude=exclude_patterns,
                loader_cls=TextLoader,
                recursive=True,
                show_progress=False,
                use_multithreading=True,
                silent_errors=True
            )
            docs.extend(loader.load())
        
        return docs
