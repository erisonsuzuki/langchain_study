import os
from langchain_core.prompts import ChatPromptTemplate

def get_prompt_template_for_task(task_name: str) -> ChatPromptTemplate:
    file_path = os.path.join("prompts", f"{task_name}.md")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        return ChatPromptTemplate.from_template(prompt_text)
    except FileNotFoundError:
        raise ValueError(f"Prompt file not found for task '{task_name}' at '{file_path}'.")
