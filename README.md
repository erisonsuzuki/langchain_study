# AI Developer Assistant (AIaaS)

A Dockerized, multi-provider AI assistant that automates complex development tasks like feature planning, documentation generation, and code analysis via a simple and powerful API.

-----

## ✨ About The Project

This project was designed to be your **personal AI assistant for software development**. The core idea is to provide a powerful yet easy-to-use tool that automates repetitive and complex tasks, allowing you to focus on the main logic of your code.

With the `AI Developer Assistant`, you can:

  - **Generate technical plans** for new features from a high-level description.
  - **Create documentation** for your projects and code files.
  - **Analyze your code** for best practices and potential improvements.
  - **Run autonomous tasks** for refactoring or editing files.

The project was built to be **provider-agnostic**, meaning you can use it with local language models (via Ollama) to ensure privacy and reduce costs, or with powerful cloud models (OpenAI, Gemini) for maximum performance. All of this is managed consistently and portably with Docker.

-----

## 💡 Features

  - 💡 **Intelligent Tasks:** Plan features, generate documentation, and analyze code using advanced AI patterns with LangChain (Conditional Chains, Agents, MapReduce).
  - 🔌 **Provider Agnostic:** Seamlessly switch between local models (Ollama) and cloud providers (OpenAI, Gemini, Anthropic) with a simple configuration.
  - 🔧 **Highly Configurable:** Control models, prompts, and LLM parameters (`temperature`, etc.) through external `.env` and `.yaml` files.
  - 📦 **Dockerized:** Get started in minutes with a consistent, portable, and isolated environment.
  - 👨‍💻 **Simple CLI Interface:** Use a clean `Makefile` as a control panel for all common operations.

-----

## 🛠️ Technologies

  - **Backend:** FastAPI
  - **AI Orchestration:** LangChain
  - **Containerization:** Docker
  - **Local LLMs:** Ollama

-----

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### 📋 Prerequisites

Ensure the following software is installed and running:

  * **[Docker](https://www.docker.com/):** Required to run the application in an isolated environment.
  * **[Ollama](https://ollama.com/):** (Optional, but recommended) To use local AI models.

### ⚙️ Installation

Follow these steps to set up the project environment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/erisonsuzuki/langchain_study.git
    cd langchain_study
    ```
2.  **Configure environment variables:**
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file to add your API keys (if using cloud providers) and set the `AI_ASSISTANT_WORKSPACE`.
3.  **Start the Ollama service (if using local models):**
    Open a separate terminal and run:
    ```bash
    OLLAMA_HOST=0.0.0.0 ollama serve
    ```
4.  **Build and run the project with Docker:**
    ```bash
    # Build the Docker image (only needed the first time or when dependencies change)
    make build

    # Start the server in the background
    make start-d

    # Check the logs to ensure the application started correctly
    make logs
    ```

The API will now be running at `http://localhost:8000`. The interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

-----

## 👨‍💻 Usage

You can interact with the `AI Developer Assistant` in two ways: through the simple `Makefile` CLI interface or by making direct HTTP requests to the API.

### 1\. Via `Makefile` (Recommended for daily use)

The `Makefile` acts as a "control panel," abstracting the complexity of API calls and Docker commands. To see all available commands, run:

```bash
make help
```

#### Usage examples:

**To plan a new feature:**

```bash
make plan desc="Create a user authentication system with password reset"
```

**To analyze a specific code file:**

```bash
make analyze file="/workspace/my-ruby-app/lib/user.rb"
```

**To generate documentation for an entire project:**

```bash
make docs path="/workspace/my-ruby-app"
```

**To instruct the code-editing agent:**

```bash
make edit instruction="Refactor the User class in user.py to include a new 'last_login' timestamp field"
```

### 2\. Via Direct HTTP Requests (Advanced)

Any external application can use the assistant by making standard HTTP requests.

**Example: Planning a feature with a model override**

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

-----

## ⚙️ Model Configuration

This assistant is provider-agnostic. You can configure it to use powerful local models via **Ollama** for privacy and cost savings, or cutting-edge cloud models for maximum performance.

The table below suggests models for each task and how to configure them in your `.env` file:

| Task / Agent | Primary Function | 🏆 Recommended Ollama Model | ☁️ Cloud Equivalents (OpenAI / Google) |
| :--- | :--- | :--- | :--- |
| **Planning Service** | Generates technical plans and user stories. | `llama3:8b` | `gpt-4o` / `gemini-1.5-pro` |
| **Documentation Service** | Summarizes code and generates a `README.md`. | `llama3:8b` | `gpt-4o` / `gemini-1.5-pro` |
| **Analysis Service** | Analyzes code for best practices. | `codegemma` | `gpt-4o` / `gemini-1.5-pro` |
| **Editing Service** | Autonomous agent for reading and modifying files. | `llama3.1:8b` | `gpt-4o` / `gemini-1.5-pro` |

-----

## 🤝 Contribution

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.
