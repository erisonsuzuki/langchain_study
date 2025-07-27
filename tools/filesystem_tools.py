import os
from langchain.tools import tool

@tool
def list_files(directory: str = '.') -> str:
    """
    Lists all files and directories in a given directory path to understand the project structure.
    """
    try:
        if ".." in directory:
            return "Error: Directory traversal is not allowed."
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def read_file(file_path: str) -> str:
    """
    Reads the complete content of a specific file to understand its code.
    """
    try:
        if ".." in file_path:
            return "Error: Directory traversal is not allowed."
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes or overwrites the content of a file. Use this to apply code changes.
    """
    try:
        if ".." in file_path:
            return "Error: Directory traversal is not allowed."
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{file_path}' saved successfully."
    except Exception as e:
        return f"Error writing to file: {e}"
