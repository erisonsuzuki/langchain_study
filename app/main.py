import argparse
from app.chains.joke_chain import get_joke_chain
from app.core.config import get_openai_api_key, get_google_api_key

# Model imports
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama

def get_llm(model_provider: str):
    """
    Initializes and returns the specified LLM.
    """
    if model_provider == "openai":
        get_openai_api_key()  # Ensure key exists
        return ChatOpenAI(model="gpt-3.5-turbo")
    elif model_provider == "google":
        api_key = get_google_api_key()
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=api_key)
    elif model_provider == "ollama":
        # Assumes Ollama is running locally.
        # You can specify a model like "llama3" or "mistral"
        return ChatOllama(model="llama3")
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}. Choose 'openai', 'google', or 'ollama'.")

def run(model_provider: str):
    """
    Runs the joke generation application with the specified model provider.
    """
    try:
        print(f"Using model provider: {model_provider}")
        llm = get_llm(model_provider)
        chain = get_joke_chain(llm)
        
        topic = "a software engineer"
        print(f"Asking for a joke about: {topic}...")
        
        response = chain.invoke({"topic": topic})
        
        print("\n--- JOKE ---")
        print(response)
        print("------------\n")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a joke using a specified LLM provider.")
    parser.add_argument(
        "provider",
        type=str,
        choices=["openai", "google", "ollama"],
        help="The model provider to use."
    )
    args = parser.parse_args()
    
    run(args.provider)
