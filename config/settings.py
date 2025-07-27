import os
import yaml
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

def _load_yaml_config(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise IOError(f"Error loading or parsing YAML file {file_path}: {e}")

LLM_SETTINGS_CONFIG = _load_yaml_config("config/llm_settings.yaml")

def get_prompt_template_for_task(task_name: str) -> ChatPromptTemplate:
    file_path = os.path.join("prompts", f"{task_name}.md")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        return ChatPromptTemplate.from_template(prompt_text)
    except FileNotFoundError:
        raise ValueError(f"Prompt file not found for task '{task_name}' at '{file_path}'.")

def get_llm_settings_for_task(task_name: str) -> dict:
    default_settings = LLM_SETTINGS_CONFIG.get("default", {})
    task_settings = LLM_SETTINGS_CONFIG.get("tasks", {}).get(task_name, {})
    final_settings = default_settings.copy()
    final_settings.update(task_settings)
    return final_settings

def get_llm_instance(provider: str, model_name: str, llm_settings: dict) -> BaseChatModel:
    provider_upper = provider.upper()
    
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    os.environ.setdefault("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    os.environ.setdefault("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))

    match provider_upper:
        case "OLLAMA":
            from langchain_ollama import ChatOllama
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return ChatOllama(model=model_name, base_url=base_url, **llm_settings)
        case "OPENAI":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model_name=model_name, **llm_settings)
        case "GEMINI":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model=model_name, convert_system_message_to_human=True, **llm_settings)
        case "ANTHROPIC":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model_name=model_name, **llm_settings)
        case _:
            raise ValueError(f"Unknown provider: '{provider}'. Valid: OLLAMA, OPENAI, GEMINI, ANTHROPIC.")

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
