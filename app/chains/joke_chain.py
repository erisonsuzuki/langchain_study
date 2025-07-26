from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from app.prompts.templates import get_joke_prompt_template

def get_joke_chain(llm: BaseChatModel):
    """
    Creates and returns a LangChain chain that generates a joke using a provided LLM.
    
    This chain combines the prompt template, the LLM, and an output parser.
    
    Args:
        llm: An instance of a class that inherits from BaseChatModel (e.g., ChatOpenAI, ChatGoogleGenerativeAI, ChatOllama).
        
    Returns:
        A runnable chain instance.
    """
    prompt = get_joke_prompt_template()
    output_parser = StrOutputParser()
    
    return prompt | llm | output_parser
