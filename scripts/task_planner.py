from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
from config.settings import get_prompt_template_for_task

def run_smart_feature_planning(llm: BaseChatModel, entry_prompt: ChatPromptTemplate, feature_description: str) -> str:
    """
    Runs an advanced feature planning workflow using a conditional chain.
    """
    backend_prompt = get_prompt_template_for_task("planning_backend")
    frontend_prompt = get_prompt_template_for_task("planning_frontend")

    classifier_chain = entry_prompt | llm | StrOutputParser()
    backend_chain = backend_prompt | llm | StrOutputParser()
    frontend_chain = frontend_prompt | llm | StrOutputParser()

    branch = RunnableBranch(
        (lambda x: "backend" in x["classification"].lower(), backend_chain),
        (lambda x: "frontend" in x["classification"].lower(), frontend_chain),
        backend_chain  # Fallback
    )

    full_chain = {"classification": classifier_chain, "feature": lambda x: x["feature"]} | branch
    return full_chain.invoke({"feature": feature_description})
