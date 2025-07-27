# AI Developer Assistant (AIaaS) - Final Version

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project implements a Dockerized "AI Assistant as a Service". It exposes various development automation capabilities (code analysis, documentation generation, feature planning, and code editing) through a RESTful API, using FastAPI.

The system is designed to be LLM provider-agnostic, allowing the use of local models via **Ollama** or cloud providers like **OpenAI**, **Google Gemini**, and **Anthropic** through a flexible configuration system.

## Architecture and Core Concepts

The architecture is designed to be modular, configurable, and extensible, based on the following pillars:

- **API-First with FastAPI:** The project's core is a web server that exposes all functionalities through a RESTful API.
- **Containerization with Docker:** The entire application is packaged into a Docker image, ensuring a consistent and portable execution environment.
- **Provider-Agnostic LLM Factory:** An abstraction layer in `config/settings.py` allows the application to dynamically use different LLM providers (Ollama, OpenAI, etc.).
- **Externalized Configuration:** Prompts (`prompts/*.md`), LLM parameters (`config/llm_settings.yaml`), and secrets (`.env`) are all managed outside the source code for maximum flexibility.
- **Development Environment with Volume Mount:** The development mode (`make start-dev`) mounts the local project inside the container, allowing the AI agents to read and modify your files in real-time.
- **Command Interface with `Makefile`**: A `Makefile` serves as a "control panel," offering simple and memorable commands for complex tasks.

## Project Structure

```bash
/ai_developer_assistant
├── Makefile              # Control panel with simple commands
├── Dockerfile            # Recipe to build the API's Docker image
├── .env.example          # Example file for environment configuration
├── README.md             # This documentation
├── requirements.txt      # List of project's Python dependencies
├── api_main.py           # The FastAPI server, API's entry point
├── config/               # Central configuration module
│   ├── llm_settings.yaml # LLM parameters (temperature, etc.)
│   └── settings.py       # Logic to load configs and create LLM instances
├── prompts/              # Directory containing all prompts in .md format
│   └── ...
├── scripts/              # Scripts with task logic and the API client
│   └── ...
└── tools/                # Tools for the AI agents
    └── ...
```

## Setup and Execution

Follow these steps to get the assistant up and running.

### 1. Environment Configuration

First, prepare your local environment.

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit the .env file to add your API keys and configure default models
nano .env
```

### 2. Starting the Ollama Server (Optional)

If you plan to use local models, open a **separate** terminal and start the Ollama service.

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

### 3. Building the Docker Image

This step only needs to be run once, or whenever you change the source code or dependencies.

```bash
make build
```

### 4. Starting the API Server

You have two ways to start the server, depending on your needs.

#### Standard API Mode (`make start-d`)

Use this mode for tasks that **do not** need to modify your local files, such as feature planning or simple analysis.

```bash
make start-d
```

#### Development Mode for Agents (`make start-dev`)

Use this command when you will be running tasks that need to **read and write to your project files**, like the code editing agent.

```bash
make start-dev
```

This command starts the server and mounts your current project directory into the container at `/app/workspace`.

## Usage

With the server running, open a **new terminal** and use the `make` commands to interact with the API. To see all available commands, type `make help`.

### Example 1: Plan a Feature (any server mode)

```bash
make plan desc="Add an email notification system for new orders"
```

### Example 2: Edit Code with the Agent

**Prerequisite:** The server must have been started with `make start-dev`.

```bash
make edit instruction="Refactor the User class in src/models.py to use Pydantic instead of dataclasses"
```

The agent will now operate on the files on your host machine, applying the changes directly.

### Stopping the Server

To stop the container running in the background:

```bash
make stop
```
