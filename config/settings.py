import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _load_yaml_config(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise IOError(f"Error loading or parsing YAML file {file_path}: {e}")

LLM_SETTINGS_CONFIG = _load_yaml_config("config/llm_settings.yaml")

def get_llm_settings_for_task(task_name: str) -> dict:
    default_settings = LLM_SETTINGS_CONFIG.get("default", {})
    task_settings = LLM_SETTINGS_CONFIG.get("tasks", {}).get(task_name, {})
    final_settings = default_settings.copy()
    final_settings.update(task_settings)
    return final_settings

def resolve_model_for_task(task_name: str, requested_model_identifier: str | None = None) -> tuple[str, str]:
    if requested_model_identifier:
        try:
            provider, model_name = requested_model_identifier.split(":", 1)
            return provider, model_name
        except ValueError:
            raise ValueError("Invalid model identifier format in request.")

    task_specific_env_var = f"{task_name.upper()}_MODEL_IDENTIFIER"
    task_specific_identifier = os.getenv(task_specific_env_var)
    if task_specific_identifier:
        try:
            provider, model_name = task_specific_identifier.split(":", 1)
            return provider, model_name
        except ValueError:
            raise ValueError(f"Invalid identifier format in env var {task_specific_env_var}.")

    provider = os.getenv("DEFAULT_PROVIDER", "OLLAMA")
    model_name = os.getenv("DEFAULT_MODEL_NAME", "llama3:8b")
    return provider, model_name
