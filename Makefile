# --- Variáveis de Configuração ---
# --- .env Loader ---
ifneq (,$(wildcard ./.env))
    include ./.env
    export
endif

# --- Configuration Variables ---
IMAGE_NAME := ai-assistant
IMAGE_TAG := final
CONTAINER_NAME := ai_assistant_server
API_CLIENT := python scripts/api_client.py

# --- Workspace Configuration Logic (Hierarchy) ---
WORKSPACE_PATH := $(or $(path),$(AI_ASSISTANT_WORKSPACE),$(HOME))

# --- Docker Lifecycle Commands ---
.PHONY: build start start-d stop logs
build: ## Build the Docker image for the application.
	@echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
	@docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

start-d: ## Start the server in detached mode, mounting a workspace.
	@echo "Starting AI Assistant server in detached mode..."
	@echo "Mapping host path '${WORKSPACE_PATH}' to '/workspace' inside the container."
	@docker run -d --rm -p 0.0.0.0:8000:8000 --env-file ./.env \
	  --add-host=host.docker.internal:host-gateway \
	  --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

start-dev: ## Start the server in detached mode, mounting a workspace.
	@echo "Starting AI Assistant server in detached mode..."
	@echo "Mapping host path '${WORKSPACE_PATH}' to '/workspace' inside the container."
	@docker run -d --rm -p 8000:8000 --env-file ./.env \
	  --add-host=host.docker.internal:host-gateway \
	  -v "${WORKSPACE_PATH}:/workspace" \
	  --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

start: ## Start the API server in the foreground, mounting a workspace.
	@echo "Starting AI Assistant server..."
	@echo "Mapping host path '${WORKSPACE_PATH}' to '/workspace' inside the container."
	@docker run --rm -p 0.0.0.0:8000:8000 --env-file ./.env \
	  --add-host=host.docker.internal:host-gateway \
	  -v "${WORKSPACE_PATH}:/workspace" \
	  --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

stop: ## Stop the detached API server container.
	@echo "Stopping AI Assistant server..."
	@docker stop ${CONTAINER_NAME}

logs: ## Follow the logs of the detached server.
	@echo "Showing logs for AI Assistant server..."
	@docker logs -f ${CONTAINER_NAME}

# --- API Task Commands (User-Friendly Facade) ---
.PHONY: plan docs analyze edit task

plan: ## Plan a new feature. Usage: make plan desc="Your feature description".
	@echo "Running feature planning..."
	@${API_CLIENT} planning '{"description": "${desc}"}' $(if ${model},--model ${model},)

docs: ## Generate documentation. Usage: make docs path="/workspace/src".
	@echo "Running documentation generation for path: ${path}..."
	@${API_CLIENT} documentation '{"project_path": "${path}"}' $(if ${model},--model ${model},)

analyze: ## Analyze a specific file. Usage: make analyze file="/workspace/src/main.py".
	@echo "Running code analysis for file: ${file}..."
	@${API_CLIENT} analysis '{"file_path": "${file}"}' $(if ${model},--model ${model},)

edit: ## Instruct the AI agent to edit code. Usage: make edit instruction="Your instruction".
	@echo "Dispatching code editing agent..."
	@${API_CLIENT} editing '{"instruction": "${instruction}"}' $(if ${model},--model ${model},)

optimizer: ## Optimizes a raw prompt. Usage: make optimizer prompt="your raw prompt".
	@echo "Running prompt optimizer..."
	@${API_CLIENT} optimizer '{"raw_prompt": "${prompt}"}' $(if ${model},--model ${model},)
	
# --- Help Command ---
.PHONY: help
help: ## Show this help message.
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
