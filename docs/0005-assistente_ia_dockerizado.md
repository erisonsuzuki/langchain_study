# AI Development Assistant (AIaaS)

This project implements a Dockerized "AI Assistant as a Service". It exposes various development automation capabilities (code analysis, documentation generation, feature planning, etc.) through a RESTful API, using FastAPI and local LLMs via Ollama.

The tool is designed to be a portable, private, and highly customizable development assistant that can be integrated into various workflows, such as CI/CD pipelines, bots, or called directly via the command line.

## Architecture and Key Concepts

The project's architecture is based on a decoupled client-server model, ensuring portability and efficiency.

1.  **AI Engine (Host Machine):** The **Ollama** service runs on the host machine (your computer). It is responsible for managing and executing the heavy language models (LLMs), utilizing the GPU's VRAM.
2.  **Application Server (Docker Container):** The Docker image contains a lightweight Python environment with **FastAPI**. It acts as the web server exposing the API endpoints (e.g., `/plan-feature`, `/generate-docs`).
3.  **Task Orchestrator (`api_main.py`):** Inside the container, this script receives API requests, interprets which task to execute, and calls the appropriate AI module.
4.  **AI Modules (`scripts/`):** Each file in the `scripts` folder is a task specialist. It contains the logic, prompt engineering, and communication with Ollama to perform a specific function.
5.  **Client:** Any application that can make an HTTP request (`curl`, a GitHub Actions pipeline, a Slack bot, etc.).

The container acts as a **lightweight, intelligent client** that connects to your **robust, local Ollama server**. This separation is the key to an efficient and flexible system.

### Project Structure

```
/advanced_ai_assistant
├── Dockerfile              # Defines the application environment
├── .gitignore              # Specifies files to be ignored by Git
├── README.md               # This documentation
├── requirements.txt        # List of Python dependencies
├── api_main.py             # FastAPI server, API entry point
└── scripts/
    ├── __init__.py         # Makes 'scripts' a Python package
    ├── code_analyzer.py    # Logic for best practices analysis
    ├── code_editor.py      # Logic for code editing
    ├── doc_generator.py    # Logic for documentation generation
    └── task_planner.py     # Logic for feature planning
```

## Basic Commands

Follow these steps to get the service up and running.

### 1\. Start the Ollama Server (on your Host Computer)

Ollama needs to be running and accessible over the network. **Open a terminal** on your machine and run:

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

**(Note: The syntax for setting environment variables may vary slightly between shells. For example, in Windows PowerShell, the command would be `$env:OLLAMA_HOST="0.0.0.0"; ollama serve`)**

**Keep this terminal window open.** It is your LLM server.

### 2\. Build the Docker Image

In your **development terminal**, at the project root, build the image:

```bash
docker build -t ai-assistant:latest .
```

### 3\. Run the API Container

Still in your **development terminal**, start the container. This command will expose port 8000 and connect the container to the Ollama service running on your host.

```bash
docker run --rm -p 8000:8000 \
  -v "$(pwd):/app" \
  -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  --name ai_assistant_server \
  ai-assistant:latest
```

  * `-p 8000:8000`: Maps port 8000 of the container to port 8000 on your machine.
  * `-v "$(pwd):/app"`: Mounts the current project directory into the `/app` folder inside the container. This is useful for development as changes to your scripts are reflected instantly. For production, you would remove this volume mount.
  * `-e OLLAMA_BASE_URL=...`: Passes the Ollama server address to the container. `host.docker.internal` is a special DNS name provided by Docker Desktop (for Mac and Windows) that points to the IP address of the host machine.

### 4\. API Usage

With the server running, you can interact with it through any HTTP client, such as `curl`.

  * **Interactive Documentation:** Open your browser and navigate to [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) to see and test all endpoints.

  * **Example: Plan a Feature**

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/plan-feature' \
      -H 'Content-Type: application/json' \
      -d '{
        "description": "Add Google social login to our app",
        "model": "llama3:8b"
      }'
    ```

  * **Example: Generate Project Documentation**
    *(This command assumes you started the container by mounting another project's volume, e.g., `-v /path/to/your/other_project:/project_to_scan`)*

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/generate-docs' \
      -H 'Content-Type: application/json' \
      -d '{
        "project_path": "/project_to_scan",
        "model": "llama3:8b"
      }'
    ```

## Debugging Workflow

If the container fails to start (e.g., `curl` fails with "connection refused/timed out"), follow these steps:

1.  **Run the container without the `--rm` flag and with `-d` (detached):**
    ```bash
    docker run -d -p 8000:8000 ... ai-assistant:latest
    ```
2.  **Check stopped containers:**
    ```bash
    docker ps -a
    ```
    Look for your container and see if its status is `Exited`.
3.  **Read the logs to find the error:**
    ```bash
    docker logs ai_assistant_server
    ```
4.  **Clean up the container after debugging:**
    ```bash
    docker rm ai_assistant_server
    ```

## How to Add New Tools

Expanding the assistant is simple:

1.  **Create a new Python script** in the `scripts/` folder with your new task's logic.
2.  **Import your new function** into `api_main.py`.
3.  **Add a new endpoint** in `api_main.py` that calls your function.
4.  **Rebuild the Docker image** with `docker build -t ai-assistant:latest .` to apply the changes.
