# Makefile (Final version with Docker networking and CURDIR fix)

# --- Configuration Variables ---
IMAGE_NAME := ai-assistant
IMAGE_TAG := final
CONTAINER_NAME := ai_assistant_server

# --- Docker Lifecycle Commands ---
.PHONY: build start-d stop logs start-dev

build: ## Build the Docker image for the application.
	@echo "--> Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
	@docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

start-dev: ## Start the dev server with the current project mounted as a workspace.
	@echo "--> Starting AI Assistant dev server..."
	@docker run -d --rm -p 8000:8000 --env-file ./.env \
	  --add-host=host.docker.internal:host-gateway \
	  -v "$(CURDIR):/app/workspace" \
	  --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

start-d: ## Start the standard API server in detached mode.
	@echo "--> Starting AI Assistant server in detached mode..."
	@docker run -d --rm -p 8000:8000 --env-file ./.env \
	  --add-host=host.docker.internal:host-gateway \
	  --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

stop: ## Stop the detached API server container.
	@echo "--> Stopping AI Assistant server..."
	@docker stop ${CONTAINER_NAME} || true

logs: ## Follow the logs of the detached server.
	@echo "--> Showing logs for AI Assistant server..."
	@docker logs -f ${CONTAINER_NAME}

# --- API Task Commands ---
.PHONY: plan docs analyze edit check_task
plan: ## Plan a new feature. Usage: make plan desc="Your feature description".
	@echo "--> Running feature planning..."
	@python scripts/api_client.py plan "${desc}"
docs: ## Generate documentation. Usage: make docs path="/app/workspace".
	@echo "--> Running documentation generation for path: ${path}..."
	@python scripts/api_client.py docs "${path}"
analyze: ## Analyze a specific file. Usage: make analyze file="/app/workspace/some_file.py".
	@echo "--> Running code analysis for file: ${file}..."
	@python scripts/api_client.py analyze "${file}"
edit: ## Instruct the AI agent to edit code. Usage: make edit instruction="Your instruction".
	@echo "--> Dispatching code editing agent..."
	@python scripts/api_client.py edit "${instruction}"
check_task: ## Check the status of a submitted task. Usage: make check_task task_id="your-task-id".
	@if [ -z "${task_id}" ]; then \
		echo "Error: Please provide a task_id (e.g., make check_task task_id=...)" && exit 1; \
	fi
	@echo "--> Checking status for task: ${task_id}"
	@curl -s http://localhost:8000/tasks/${task_id} | python -m json.tool

# --- Help Command ---
.PHONY: help
help: ## Show this help message.
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
