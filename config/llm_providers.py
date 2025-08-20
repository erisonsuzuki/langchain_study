import os
from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

class LLMProvider(ABC):
    @abstractmethod
    def create_llm(self, model_name: str, llm_settings: dict) -> BaseChatModel:
        pass

class OllamaProvider(LLMProvider):
    def create_llm(self, model_name: str, llm_settings: dict) -> BaseChatModel:
        from langchain_ollama import ChatOllama
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=model_name, base_url=base_url, **llm_settings)

class OpenAIProvider(LLMProvider):
    def create_llm(self, model_name: str, llm_settings: dict) -> BaseChatModel:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=model_name, **llm_settings)

class GeminiProvider(LLMProvider):
    def create_llm(self, model_name: str, llm_settings: dict) -> BaseChatModel:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model_name, convert_system_message_to_human=True, **llm_settings)

class AnthropicProvider(LLMProvider):
    def create_llm(self, model_name: str, llm_settings: dict) -> BaseChatModel:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model_name=model_name, **llm_settings)

LLM_PROVIDERS: dict[str, LLMProvider] = {
    "OLLAMA": OllamaProvider(),
    "OPENAI": OpenAIProvider(),
    "GEMINI": GeminiProvider(),
    "ANTHROPIC": AnthropicProvider(),
}

def get_llm_instance(provider: str, model_name: str, llm_settings: dict) -> BaseChatModel:
    provider_upper = provider.upper()
    if provider_upper not in LLM_PROVIDERS:
        raise ValueError(f"Unknown or unsupported provider: '{provider}'. Supported: {list(LLM_PROVIDERS.keys())}")
    return LLM_PROVIDERS[provider_upper].create_llm(model_name, llm_settings)
