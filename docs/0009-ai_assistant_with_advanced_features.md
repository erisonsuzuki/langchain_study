# Advanced Features & Architectural Patterns

This document details the advanced software engineering and AI patterns used within the AI Developer Assistant. 

## 1. SOLID, Service-Oriented Architecture

To ensure the project is maintainable, testable, and scalable, the codebase was refactored into a professional, multi-layered architecture based on SOLID principles.

-   **Core Idea:** The logic for each task is encapsulated within its own **Service** class in the `services/` directory. The API layer (`api_main.py`) acts as a thin controller that delegates all business logic to the Service Layer, using FastAPI's Dependency Injection system.

-   **Key Principles Applied:**
    -   **Single Responsibility Principle (SRP):** Each service (e.g., `PlanningService`) has only one job.
    -   **Dependency Inversion Principle (DIP):** The API layer depends on service abstractions, not concrete classes.
    -   **Liskov Substitution Principle (LSP):** All LLM provider classes are used interchangeably as `BaseChatModel` instances.

## 2. Advanced LangChain Patterns in Action

To elevate the assistant from a simple text generator to a complex problem-solver, we implemented several advanced LangChain patterns.

### A. Conditional Logic with Dynamic Routing for Smart Task Planning
-   **Task Improved:** Feature Planning (`services/planning_service.py`)
-   **Problem Solved:** A simple planner treats all requests the same. A request to "change a button color" (frontend) received the same process as one to "add a new database table" (backend).
-   **The Solution:** The planning service now uses a sophisticated conditional chain with **dynamic routing**.

    1.  **Classification:** A dedicated `classifier_chain` first analyzes the user's request to determine its category (e.g., `frontend`, `backend`).
    2.  **Data Passthrough:** Using `RunnablePassthrough.assign`, we run the classifier while ensuring the original feature description is preserved and passed along for the next step. This creates a temporary data structure like `{"feature": "...", "classification": "frontend"}`.
    3.  **Dynamic Routing:** A Python function wrapped in a `RunnableLambda` acts as a smart router. It inspects the `classification` from the previous step and dynamically selects the appropriate specialist chain (`frontend_chain` or `backend_chain`) to execute next.
    4.  **Execution:** The chosen specialist chain is then invoked with the complete data, ensuring it has access to the original feature description.

    This LCEL pattern is highly robust and ensures a clean separation between the routing logic and the task-specific execution chains.

    *Conceptual LCEL Structure:*
    ```python
    def route(info):
        if "backend" in info["classification"].lower():
            return backend_chain
        else:
            return frontend_chain

    full_chain = (
        RunnablePassthrough.assign(
            classification=({"feature": lambda x: x["feature"]} | classifier_chain)
        )
        | RunnableLambda(route)
    )
    ```

### B. Autonomous Agents with Tools for Code Editing
-   **Task Improved:** Code Editing (`services/editing_service.py`)
-   **Problem Solved:** A simple chain can only *suggest* code changes. It is "blind" to the project's actual file structure and content.
-   **The Solution:** The editing task is powered by a **ReAct Agent**.
    1.  **Tools:** The agent is given access to tools defined in `tools/filesystem_tools.py`, such as `list_files`, `read_file`, and `write_file`.
    2.  **Reasoning Loop:** The agent follows a `Thought -> Action -> Observation` loop. It can decide to `list_files` to understand the project, then `read_file` to get the necessary context, and only then, once it has a complete picture, `write_file` to apply the changes.
    3.  **Result:** This transforms the editor from a simple text generator into an autonomous agent capable of reasoning and interacting with its environment to complete complex tasks.

### C. Scalable Processing with Map-Reduce Chains
-   **Task Improved:** Documentation Generation (`services/docs_service.py`)
-   **Problem Solved:** Large projects would exceed the LLM's context window, making it impossible to generate a complete document in one go.
-   **The Solution:** The documentation service uses the **Map-Reduce** pattern.
    1.  **Map Step:** The service iterates through each source file and makes a separate, parallel LLM call to generate a concise summary for that single file.
    2.  **Reduce Step:** All the individual summaries are then gathered and passed in a final LLM call, which has the task of combining these summaries into a single, cohesive `README.md`.
    3.  **Result:** This allows the assistant to generate documentation for projects of virtually any size.

## 3. Structured and Validated Outputs (`PydanticOutputParser`)

-   **Problem Solved:** Raw LLM output can be inconsistent and unstructured, making it unreliable for applications.
-   **The Solution:** Most services use LangChain's `PydanticOutputParser`.
    1.  **Schema Definition:** For each task, a Pydantic model defines the exact JSON structure of the desired output (e.g., `{"plan_markdown": "..."}`).
    2.  **Prompt Injection & Validation:** The parser automatically adds formatting instructions to the prompt and validates that the LLM's output conforms to the schema, preventing malformed data.
    3.  **Result:** This creates a reliable "API contract" between the AI and the application, ensuring all outputs are structured and ready for use.
