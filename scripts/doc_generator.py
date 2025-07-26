# scripts/doc_generator.py
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_doc_generation(project_path: str, model_name: str, ollama_base_url: str) -> str:
    all_code = ""
    valid_extensions = ('.py', '.rb', '.js', '.go', '.ts', '.java')
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        all_code += f"--- Content of {file_path} ---\n{f.read()}\n\n"
                except Exception:
                    continue

    if not all_code:
        return "No source code files found in the specified path."

    llm = ChatOllama(model=model_name, temperature=0.1, base_url=ollama_base_url)
    prompt = ChatPromptTemplate.from_template("""
    You are a Senior Technical Writer. Your task is to create a complete and professional README.md file for a software project.
    Based on all the source code provided below, generate the documentation.

    **Full Source Code:**
    {code}

    **README.md Structure:**
    1.  **Project Title**
    2.  **Description**
    3.  **Core Features**
    4.  **How to Use**

    Respond ONLY with the content of the README.md file in Markdown format.
    """)
    chain = prompt | llm | StrOutputParser()
    readme_content = chain.invoke({"code": all_code})
    
    # In a real scenario, you would save this to a file.
    # For the API, we return the content.
    return readme_content
