# AI Developer Assistant - Functional Documentation

## 1. Overview

This document provides a detailed explanation of the features and capabilities of the AI Developer Assistant. This system is designed as an API-first, provider-agnostic service to automate and enhance various stages of the software development lifecycle.

For instructions on setup, installation, and basic commands, please refer to the `README.md` file.

## 2. Core Architectural Concepts

The assistant's functionality is built upon several key architectural principles:

  * **Provider-Agnostic LLM Factory:** The system is not tied to a single LLM provider. A central "factory" can instantiate models from Ollama (local), OpenAI, Google Gemini, or Anthropic based on configuration settings. This allows for using the best model for each specific task.
  * **Task-Specific Logic:** Each core functionality (planning, analysis, etc.) is encapsulated in its own script and uses dedicated prompts. This makes the system modular and easy to extend.
  * **Externalized Configuration:** All prompts (in `prompts/*.md`), LLM parameters (in `config/llm_settings.yaml`), and environment settings (in `.env`) are external to the application code, allowing for easy tuning and maintenance.
  * **Asynchronous Task Handling:** For long-running operations like documentation generation and agent-based code editing, the API uses a background task system. It immediately returns a `task_id`, allowing the client to check the status and retrieve the result later without a hanging connection.

-----

## 3. Functionalities / API Endpoints

### 3.1. Smart Feature Planner

  * **Endpoint:** `POST /plan-feature`
  * **Purpose:** To convert a high-level feature idea into a structured, actionable technical plan for the development team. This saves time in sprint planning and ensures requirements are well-defined.
  * **Internal Workflow (Conditional Chain):** This is a multi-step, intelligent process:
    1.  **Classification:** The initial feature description is first sent to an LLM with a classifier prompt (`prompts/planning_classifier.md`) to determine its category (e.g., `backend`, `frontend`, `fullstack`).
    2.  **Conditional Routing (`RunnableBranch`):** Based on the classification, the request is routed to a specialized prompt chain.
    3.  **Specialized Planning:** If classified as `backend`, a prompt focused on API endpoints and database schemas (`prompts/planning_backend.md`) is used. If `frontend`, a prompt focused on UI components and state management (`prompts/planning_frontend.md`) is used. This ensures the generated plan is highly relevant and detailed.
  * **Request Payload:**
    | Field | Type | Description |
    | :--- | :--- | :--- |
    | `description` | string | A high-level description of the feature. |
    | `model` | string (optional) | Override the default model (e.g., `"OPENAI:gpt-4o"`). |
  * **Successful Response:** A JSON object containing the generated plan in Markdown format and the model that was used.
  * **Usage Example:**
    ```bash
    make plan desc="Implement 2FA using authenticator apps"
    ```

### 3.2. Code Best Practices Analyzer

  * **Endpoint:** `POST /analyze-code`
  * **Purpose:** To act as an AI-powered linter that checks code for adherence to universal clean code principles that traditional linters might miss, such as clarity of variable names, function complexity, and quality of comments.
  * **Internal Workflow:**
    1.  The system detects the programming language based on the file extension.
    2.  It loads the analysis prompt from `prompts/analysis.md`, injecting the detected language for context.
    3.  The LLM analyzes the provided code against the prompt's instructions.
    4.  The response is parsed to determine a `PASSED` or `FAILED` status.
  * **Request Payload:**
    | Field | Type | Description |
    | :--- | :--- | :--- |
    | `file_path` | string | The path to the file to be analyzed *inside the container*. |
    | `model` | string (optional) | Override the default model. |
  * **Successful Response:** A JSON object with the LLM's analysis, a boolean `passed` status, and the model used.
  * **Usage Example:**
    ```bash
    make analyze file="/app/workspace/src/main.py"
    ```

### 3.3. Scalable Documentation Generator (Asynchronous)

  * **Endpoint:** `POST /generate-docs`
  * **Purpose:** To automatically create a comprehensive `README.md` file for an entire codebase, even for very large projects that would exceed the context window of a standard LLM call.
  * **Internal Workflow (`MapReduceDocumentsChain`):**
    1.  **Load:** The system recursively loads all source code files from the specified project path.
    2.  **Map Step:** It iterates through each file individually. For each file, it calls an LLM with the `docs_map.md` prompt to generate a concise summary of that file's purpose.
    3.  **Reduce Step:** All the individual summaries from the "Map" step are collected and passed as a single context to a final LLM call. This call uses the `docs_reduce.md` prompt to synthesize the summaries into a cohesive, high-level `README.md` document.
  * **Request Payload:**
    | Field | Type | Description |
    | :--- | :--- | :--- |
    | `project_path` | string | The path to the project to be documented *inside the container*. |
    | `model` | string (optional) | Override the default model. |
  * **Successful Response:** See Section 4: Handling Asynchronous Tasks.

### 3.4. Autonomous Code Editing Agent (Asynchronous)

  * **Endpoint:** `POST /edit-code-agent`
  * **Purpose:** To perform complex, multi-file code modifications based on a high-level natural language instruction. This agent can reason, plan, and interact with the filesystem to achieve its goal.
  * **Internal Workflow (ReAct Agent with Tools):**
    1.  **Initialization:** An agent is created and given access to a set of "tools" from `tools/filesystem_tools.py` (`list_files`, `read_file`, `write_file`).
    2.  **Reasoning Loop:** The agent receives the user's instruction (e.g., "Refactor the User class to use Pydantic") and begins a loop of Thought -\> Action -\> Observation:
          * **Thought:** The LLM thinks about what it needs to do first (e.g., "I need to find the User class. I should list the files in the project.").
          * **Action:** The LLM decides to call the `list_files` tool.
          * **Observation:** The agent executes the tool and feeds the result (the list of files) back to the LLM.
    3.  This loop continues as the agent reads files for context, generates the new code, and finally uses the `write_file` tool to apply the changes.
  * **Request Payload:**
    | Field | Type | Description |
    | :--- | :--- | :--- |
    | `instruction` | string | The high-level task for the agent to perform. |
    | `project_path` | string | The workspace path for the agent to operate in *inside the container*. |
    | `model` | string (optional) | Override the default model. |
  * **Successful Response:** See Section 4: Handling Asynchronous Tasks.

## 4. Handling Asynchronous Tasks

The `generate-docs` and `edit-code-agent` endpoints can take a long time to complete. They use an asynchronous, non-blocking pattern.

  * **Step 1: Submitting a Task**
    When you make a `POST` request to one of these endpoints, the server immediately accepts the job and returns a `200 OK` response with a unique `task_id`.
    **Submission Response:**

    ```json
    {
      "task_id": "docs-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "status": "submitted",
      "message": "Documentation generation started. Check status endpoint for progress."
    }
    ```

  * **Step 2: Checking the Task Status**
    You can then use the `task_id` to poll the status endpoint to see if the job is finished.

      * **Endpoint:** `GET /tasks/{task_id}`
      * **Usage Example:** `make check_task task_id="docs-xxxxxxxx..."`

    **Possible Status Responses:**

      * **Running:**
        ```json
        {
          "status": "running",
          "start_time": 1753689600.123,
          "result": null
        }
        ```
      * **Completed:**
        ```json
        {
          "status": "completed",
          "start_time": 1753689600.123,
          "result": "The final output of the task (e.g., the README content or the agent's final message).",
          "end_time": 1753689720.456
        }
        ```
