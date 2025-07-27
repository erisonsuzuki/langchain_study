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

## Usage

Interact with the assistant using the simple `make` commands.

```bash
# See all available commands
make help

# Example: Plan a new feature
make plan desc="A new dashboard for user analytics"

# Example: Generate documentation for a project located in your workspace
make docs path="/workspace/my-app"

# Stop the server when you are done
make stop
```

## Project Documentation

This project's evolution, architectural decisions, and the step-by-step process of its creation are documented in detail within the `docs/` directory.
