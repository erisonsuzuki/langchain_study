import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def run_code_analysis(llm: BaseChatModel, prompt: ChatPromptTemplate, file_path: str) -> tuple[str, bool]:
    language_map = {".py": "Python", ".rb": "Ruby", ".js": "JavaScript"}
    file_extension = os.path.splitext(file_path)[1]
    language = language_map.get(file_extension, "unknown")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}", False

    if not source_code.strip():
        return "File is empty. PASSED.", True

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"language": language, "code": source_code})
    passed = "FAILED" not in response.upper()
    return response, passed
