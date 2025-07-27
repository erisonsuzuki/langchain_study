# AI Developer Assistant (AIaaS)

[](https://github.com)
[](https://opensource.org/licenses/MIT)

A Dockerized, multi-provider AI assistant that automates complex development tasks like feature planning, documentation generation, and code analysis via a simple and powerful API.

## Key Features

  - 💡 **Intelligent Tasks:** Plan features, generate documentation, and analyze code using advanced LangChain patterns (Conditional Chains, Agents, MapReduce).
  - 🔌 **Provider Agnostic:** Seamlessly switch between local models (Ollama) and cloud providers (OpenAI, Gemini, Anthropic) via simple configuration.
  - 🔧 **Highly Configurable:** Control models, prompts, and LLM parameters (`temperature`, etc.) through external `.env` and `.yaml` files.
  - 📦 **Dockerized:** Get started in minutes with a consistent, portable, and isolated environment.
  - 👨‍💻 **Simple CLI Interface:** Use a clean `Makefile` as a control panel for all common operations.

## Tech Stack

  - **Backend:** FastAPI
  - **AI Orchestration:** LangChain
  - **Containerization:** Docker
  - **Local LLMs:** Ollama

## Quick Start

### 1. Prerequisites

  - [Docker](https://www.docker.com/) is installed and running.
  - [Ollama](https://ollama.com/) is installed (for using local models).

### 2. Environment Setup

```bash
# Clone the repository (if you haven't already)
# git clone <repository_url>
# cd ai_developer_assistant_final

# 1. Create your environment file from the example
cp .env.example .env

# 2. Edit the .env file to add your API keys and set your AI_ASSISTANT_WORKSPACE
nano .env

# 3. If using Ollama, start the service in a separate terminal
# OLLAMA_HOST=0.0.0.0 ollama serve
```

### 3. Build and Run

Use the Makefile to manage the application lifecycle.

```bash
# Build the Docker image (only needs to be done once or when dependencies change)
make build

# Start the server in the background
make start-d

# Check the logs to ensure it started correctly
make logs
```

The API is now running at `http://localhost:8000`. You can see the interactive API documentation at `http://localhost:8000/docs`.

## Recommended Models & Configuration

This assistant is provider-agnostic. You can configure it to use powerful local models via Ollama for privacy and cost-savings, or cutting-edge cloud models for maximum performance.

### Model Recommendations (Ollama vs. Cloud)

This table maps each agent/task within the assistant to the recommended local Ollama model and its high-performance cloud equivalents. You can configure these in your `.env` file using the task-specific override variables (e.g., `PLANNING_MODEL_IDENTIFIER`).

| Task / Agent | Primary Function | 🏆 Recommended Ollama Model | ☁️ Cloud Equivalents (OpenAI / Google) |
| :--- | :--- | :--- | :--- |
| **Planning Service** | Generates technical plans and user stories from a high-level description. | `llama3:8b` | `gpt-4o` / `gemini-1.5-pro` |
| **Documentation Service** | Summarizes code files and generates a complete `README.md`. | `llama3:8b` | `gpt-4o` / `gemini-1.5-pro` |
| **Analysis Service** | Analyzes code files for adherence to best practices. | `codegemma` | `gpt-4o` / `gemini-1.5-pro` |
| **Editing Service** | Acts as an autonomous agent to read, write, and modify files. | `llama3.1:8b` | `gpt-4o` / `gemini-1.5-pro` |

### How to Configure Models in `.env`

You control which model is used for each task in your `.env` file.

**1. Set the Global Default**
This is the model that will be used for any task if no specific override is set. It's great for general use.

```ini
# .env
# Use a fast local model as the default for most tasks.
DEFAULT_PROVIDER=OLLAMA
DEFAULT_MODEL_NAME=llama3:8b
```

**2. Set Task-Specific Overrides (Recommended)**
For the best results, use the optional override variables to assign a specialized model to a specific task.

```ini
# .env
# Use the global default (Ollama Llama3) for most things, but...

# ...use OpenAI's powerful GPT-4o specifically for documentation generation.
DOCS_MODEL_IDENTIFIER=OPENAI:gpt-4o

# ...and use Ollama's specialized CodeGemma for all code analysis tasks.
ANALYSIS_MODEL_IDENTIFIER=OLLAMA:codegemma
```

With this configuration, `make plan` would use `llama3:8b`, while `make docs` would use `gpt-4o`, giving you the best of both worlds.

## Usage

There are two primary ways to interact with the AI Assistant: via the convenient `Makefile` interface for daily tasks, or by making direct HTTP requests to the API for external integrations.

### 1\. Interacting via Makefile (Recommended for Daily Use)

The `Makefile` provides a simple, memorable set of commands that act as a "control panel" for the assistant. All complex Docker and API calls are handled for you.

First, see all available commands by running:

```bash
make help
```

#### Common Task Examples:

**To plan a new feature:**
The command constructs the necessary JSON payload and calls the `/tasks/planning` endpoint.

```bash
make plan desc="Create a user authentication system with password reset"
```

**To analyze a specific code file:**
Remember to use the path **inside the container**, which is prefixed with `/workspace`. This path corresponds to the `AI_ASSISSTANT_WORKSPACE` you set in your `.env` file.

```bash
make analyze file="/workspace/my-ruby-app/lib/user.rb"
```

**To generate documentation for an entire project:**

```bash
make docs path="/workspace/my-ruby-app"
```

**To instruct the code-editing agent:**
This command dispatches the autonomous agent to perform a complex task.

```bash
make edit instruction="Refactor the User class in user.py to include a new 'last_login' timestamp field"
```

### 2\. External & Direct API Interaction (Advanced)

Any external application (CI/CD pipelines, other microservices, custom scripts) can use the assistant by making standard HTTP requests with a tool like `curl`.

#### Step 1: Run the Server with the Target Workspace

First, you must start the server and mount the external project directory you want to work on. The `Makefile` helps with this.

Let's say your other project is located at `~/dev/external-project` on your host machine.

```bash
# Start the assistant, mounting the external project into the container's /workspace
make start-d path=~/dev/external-project
```

Now, the AI assistant is running and has access to the files in `~/dev/external-project` via the `/workspace` directory inside the container.

#### Step 2: Call the API using `curl`

Now you can use `curl` or any other HTTP client to call the API. You must use the in-container path.

**Example: Running the `analysis` task on an external file**

This command calls the generic `/tasks/analysis` endpoint, passing the file path inside the `data` object.

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/analysis' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
      "file_path": "/workspace/src/main.py"
    }
  }'
```

**Example: Planning a feature with a specific model override**

This command calls the `/tasks/planning` endpoint and temporarily overrides the default model to use OpenAI's GPT-4o for this specific request.

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/planning' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "OPENAI:gpt-4o",
    "data": {
      "description": "Add a two-factor authentication feature using TOTP"
    }
  }'
```

## Project Documentation

This project's evolution, architectural decisions, and the step-by-step process of its creation are documented in detail within the `docs/` directory.
