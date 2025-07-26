from langchain_core.prompts import ChatPromptTemplate

def get_joke_prompt_template():
    """
    Returns a ChatPromptTemplate for generating a joke on a given topic.
    
    Returns:
        ChatPromptTemplate: The prompt template.
    """
    return ChatPromptTemplate.from_messages([
        ("system", "You are a world-class comedian."),
        ("user", "Tell me a joke about {topic}.")
    ])
