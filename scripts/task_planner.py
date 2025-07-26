# scripts/task_planner.py
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_feature_planning(feature_description: str, model_name: str, ollama_base_url: str) -> str:
    llm = ChatOllama(model=model_name, temperature=0.3, base_url=ollama_base_url)
    prompt = ChatPromptTemplate.from_template("""
    You are a hybrid Senior Product Manager and Senior Software Architect.
    Your task is to take a high-level feature description and turn it into an initial technical plan for the development team.

    **Feature Description:**
    {feature}

    **Generate the following plan in Markdown format:**
    1.  **Feature Objective:** Summarize the user value in one sentence.
    2.  **User Stories:** Create 2-3 user stories in the format "As a [user type], I want to [perform an action], so that I can [achieve a benefit]".
    3.  **Technical Implementation Plan:**
        - **Files to Create/Modify:** List the files that will likely need to be changed or created.
        - **Data Models / DB Schema:** Suggest any necessary database changes.
        - **API Endpoints (if applicable):** Define the required API endpoints (e.g., GET /api/users).
    4.  **Acceptance Criteria:** List 3-5 points that define when the feature is "done".
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"feature": feature_description})
