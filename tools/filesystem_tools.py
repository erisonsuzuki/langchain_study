# tools/filesystem_tools.py
import os
from langchain.tools import tool

def _resolve_path(file_path: str) -> str:
    """Helper function to safely resolve paths inside the workspace."""
    clean_path = file_path.strip()
    secure_path = os.path.join("/workspace", clean_path.lstrip('/'))
    if not os.path.abspath(secure_path).startswith('/workspace'):
        raise PermissionError("Error: Directory traversal outside of /workspace is not allowed.")
    return secure_path

@tool
def list_files(directory: str = '.') -> str:
    """
    Lists all files and directories in a given directory path relative to the workspace.
    """
    try:
        resolved_dir = _resolve_path(directory)
        return "\n".join(os.listdir(resolved_dir))
    except Exception as e:
        return f"Error listing files in '{directory}': {e}"

@tool
def read_file(file_path: str) -> str:
    """
    Reads the complete content of a specific file path relative to the workspace.
    The `file_path` argument must be a valid path to a file.
    """
    try:
        resolved_path = _resolve_path(file_path)
        with open(resolved_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Writes or overwrites the content of a file at a specific path relative to the workspace.
    This tool requires two arguments:
    1. file_path (string): The full path to the file you want to write to.
    2. content (string): The new content you want to write into the file.
    """
    try:
        resolved_path = _resolve_path(file_path)
        os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
        with open(resolved_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{file_path}' saved successfully."
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"
