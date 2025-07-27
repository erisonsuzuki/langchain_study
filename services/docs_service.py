# services/docs_service.py
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from .base_service import AbstractTaskService
from core.exceptions import ServiceExecutionError
from config.settings import (
    resolve_model_for_task,
    get_llm_settings_for_task,
    get_llm_instance,
    get_prompt_template_for_task,
)
from langchain_community.document_loaders import DirectoryLoader, TextLoader


class DocsRequest(BaseModel):
    project_path: str

class DocsService(AbstractTaskService):
    """Service for scalable documentation generation using modern LCEL patterns."""
    def __init__(self, task_name: str = "documentation"):
        self.task_name = task_name

    def execute(self, project_path: str, model_override: Optional[str] = None) -> dict:
        try:
            # 1. Resolve models and settings (no changes here)
            provider, model_name = resolve_model_for_task(self.task_name, model_override)
            llm_settings = get_llm_settings_for_task(self.task_name)
            llm = get_llm_instance(provider, model_name, llm_settings)

            # 2. Load documents with the intelligent loader (no changes here)
            # ... (loader configuration from the previous step) ...
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
            
            if not docs:
                return {"docs_generated": "No relevant source code files found.", "model_used": f"{provider}:{model_name}"}

            print(f"INFO: Found {len(docs)} relevant files to process.")

            # --- REFACTORED LOGIC USING LCEL ---

            # 3. Define the "Map" chain using LCEL pipe syntax
            map_prompt = get_prompt_template_for_task("documentation_map")
            map_chain = map_prompt | llm | StrOutputParser()

            # 4. Run the "Map" step efficiently in parallel using .batch()
            print("INFO: Generating summaries for each file (Map step)...")
            map_inputs = [{"page_content": doc.page_content} for doc in docs]
            summaries = map_chain.batch(map_inputs)

            # 5. Combine the summaries for the "Reduce" step
            combined_summaries = "\n\n---\n\n".join(summaries)

            # 6. Define the "Reduce" chain using LCEL
            reduce_prompt = get_prompt_template_for_task("documentation_reduce")
            reduce_chain = reduce_prompt | llm | StrOutputParser()

            # 7. Run the "Reduce" step to get the final document
            print("INFO: Combining summaries into the final document (Reduce step)...")
            final_readme = reduce_chain.invoke({"doc_summaries": combined_summaries})

            return {"docs_generated": final_readme, "model_used": f"{provider}:{model_name}"}

        except Exception as e:
            raise ServiceExecutionError(message=f"Error in DocsService: {e}", original_exception=e)
