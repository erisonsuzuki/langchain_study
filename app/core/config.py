import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_openai_api_key():
    """
    Retrieves the OpenAI API key from environment variables.
    
    Raises:
        ValueError: If the OPENAI_API_KEY is not set.
        
    Returns:
        str: The OpenAI API key.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please create a .env file and add it.")
    return api_key

def get_google_api_key():
    """
    Retrieves the Google API key from environment variables.
    
    Raises:
        ValueError: If the GOOGLE_API_KEY is not set.
        
    Returns:
        str: The Google API key.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please update your .env file.")
    return api_key

# You can add other configurations here, for example:
# MODEL_NAME = "gemini-pro"
# TEMPERATURE = 0.7
