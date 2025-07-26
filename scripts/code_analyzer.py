# scripts/code_analyzer.py
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_code_analysis(file_path: str, model_name: str, ollama_base_url: str) -> tuple[str, bool]:
    language_map = {".py": "Python", ".rb": "Ruby", ".js": "JavaScript"}
    file_extension = os.path.splitext(file_path)[1]
    language = language_map.get(file_extension, "unknown")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}", False

    llm = ChatOllama(model=model_name, temperature=0, base_url=ollama_base_url)
    prompt = ChatPromptTemplate.from_template("""
    You are a Senior Software Architect and a Clean Code expert for the {language} language.
    Analyze the provided source code and check for violations of universal best practices (clear names, short functions, no magic numbers).

    **Source Code:**
    ```
    {code}
    ```
    If the code looks clean, respond only with "PASSED".
    If you find issues, respond with "FAILED" followed by a list of the problems.
    """)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"language": language, "code": source_code})
    
    passed = "FAILED" not in response.upper()
    return response, passed
