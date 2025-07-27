Claro, aqui está a tradução completa do conteúdo para o inglês, mantendo a formatação original.

-----

# AI Development Assistant (AIaaS)

This project implements a Dockerized "AI Assistant as a Service". It exposes various development automation capabilities (code analysis, documentation generation, feature planning, etc.) through a RESTful API, using FastAPI.

The system is designed to be **LLM provider agnostic**, allowing the use of local models via **Ollama** or cloud providers like **OpenAI**, **Google Gemini**, and **Anthropic** through a flexible and hierarchical configuration system.

## Architecture and Key Concepts

The architecture was designed to be modular, configurable, and extensible, based on the following pillars:

  * **API-First with FastAPI:** The project's core is a web server that exposes all functionalities through a RESTful API, allowing any service, script, or tool to interact with the assistant.
  * **Containerization with Docker:** The entire application is packaged into a Docker image, ensuring a consistent and portable execution environment, eliminating dependency issues between machines.
  * **Agnostic LLM Factory:** An abstraction layer (`config/settings.py`) allows the application to request an LLM instance without worrying about which provider (Ollama, OpenAI, etc.) is being used. The selection is made dynamically based on configuration files.
  * **Externalized Configuration:**
      * **`.env`**: Manages secrets (API keys) and the selection of the default provider/model.
      * **`prompts/`**: All prompts are maintained as individual `.md` files, allowing for easy editing by anyone on the team without touching the code.
      * **`config/llm_settings.yaml`**: Controls fine-grained LLM parameters (like `temperature`) for each type of task.
  * **Command Interface with `Makefile`**: A `Makefile` in the project root serves as a "control panel", offering simple and memorable commands for complex tasks like building the Docker image, starting the server, and interacting with the API.

## Project Structure

```
/ai_assistant_final
├── Makefile                # Control panel with simple commands (make start, make plan)
├── Dockerfile              # Recipe to build the API server's Docker image
├── .env.example            # Example file for environment configuration
├── .gitignore              # Specifies files to be ignored by Git
├── .pre-commit-config.yaml # Configuration for Git hooks (code quality)
├── README.md               # This documentation
├── requirements.txt        # List of the project's Python dependencies
├── api_main.py             # The FastAPI server, the API's entry point
├── config/                 # Central configuration module
│   ├── llm_settings.yaml   # LLM parameters (temperature, etc.)
│   └── settings.py         # Logic for loading configs, prompts, and creating LLM instances
├── prompts/                # Directory containing all prompts
│   ├── analysis.md         # Prompt for the code analysis task
│   ├── documentation.md    # Prompt for the documentation generation task
│   └── planning.md         # Prompt for the feature planning task
└── scripts/
    └── api_client.py       # Command-line client to interact with the API
```

## Installation and Execution

Follow these steps to get the assistant up and running.

### Prerequisites

1.  **Docker** installed and running.
2.  **Ollama** installed locally (if you plan to use local models).
3.  **Git** to clone the repository.

### 1\. Environment Setup

First, clone the repository and set up your local environment.

```bash
# Clone the project (if applicable)
# git clone ...
# cd ai_assistant_final

# 1. Create your environment file from the example
cp .env.example .env

# 2. Edit the .env file to add your API keys and configure the default models
nano .env
```

### 2\. Starting the Server with Ollama (if applicable)

If you plan to use local models, open a **separate** terminal and start the Ollama service so it accepts network connections.

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

### 3\. Building and Starting the AI Assistant

With the `Makefile`, this process is very simple.

```bash
# Build the Docker image. This only needs to be done once or when the code changes.
make build

# Start the server in the background ("detached" mode)
make start-d

# Check the logs to ensure everything started correctly
make logs
```

Your "AI Assistant as a Service" is now running and accessible at `http://localhost:8000`.

## How to Use the Features

The easiest way to interact with the project is through the `make` commands. To see all available commands, run:

```bash
make help
```

### Command Examples

#### Plan a New Feature

```bash
make plan desc="Add an email notification system for new orders"
```

This command sends the description to the `/plan-feature` endpoint of your API, which will use the configured planning model and return a detailed technical plan.

#### Generate Documentation for a Project

To use this feature, you need to run the container by mounting the volume of the project you want to document. The `Makefile` can be adapted for this, but a direct `docker` call illustrates the concept:

```bash
# Stop the current server if it is running
make stop

# Start the server by mounting the target project into the /target_project folder
docker run -d --rm -p 8000:8000 --env-file ./.env \
  -v "/full/path/to/your/other/project:/target_project" \
  --name ai_assistant_server \
  ai-assistant:latest

# Now, call the 'make' command
make docs path="/target_project"
```

#### Stop the Server

```bash
make stop
```

## Advanced Configuration

The assistant's flexibility comes from its external configuration capabilities.

  * **`prompts/*.md`**: To change the behavior of a task, simply edit the corresponding prompt file. For example, to make the feature planner more or less detailed, edit `prompts/planning.md`. No server restart is needed.
  * **`config/llm_settings.yaml`**: To adjust the "creativity" (temperature) or other parameters of a model for a specific task, edit this file.
  * **`.env`**: This file controls everything. You can change the default provider from `OLLAMA` to `OPENAI` by changing the `DEFAULT_PROVIDER` variable. You can force a specific task to use a different model by setting, for example, `DOCS_MODEL_IDENTIFIER=GEMINI:gemini-1.5-pro`. The system will apply the changes the next time the container is started.
