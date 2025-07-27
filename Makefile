# Makefile for the AI Assistant project

# --- Configuration Variables ---
IMAGE_NAME := ai-assistant
IMAGE_TAG := final
CONTAINER_NAME := ai_assistant_server
API_CLIENT := python scripts/api_client.py

# --- Docker Lifecycle Commands ---
.PHONY: build start start-d stop logs
build: ## Build the Docker image for the application.
	@echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
	@docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

start: ## Start the API server in the foreground.
	@echo "Starting AI Assistant server..."
	@docker run --rm -p 8000:8000 --env-file ./.env --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

start-d: ## Start the API server in detached (background) mode.
	@echo "Starting AI Assistant server in detached mode..."
	@docker run -d --rm -p 8000:8000 --env-file ./.env --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}

stop: ## Stop the detached API server container.
	@echo "Stopping AI Assistant server..."
	@docker stop ${CONTAINER_NAME}

logs: ## Follow the logs of the detached server.
	@echo "Showing logs for AI Assistant server..."
	@docker logs -f ${CONTAINER_NAME}

# --- API Task Commands ---
.PHONY: plan docs analyze

plan: ## Plan a new feature. Usage: make plan desc="Your feature description".
	@echo "Running feature planning..."
	@${API_CLIENT} plan "${desc}"

docs: ## Generate documentation for a project path. Usage: make docs path="/project/src".
	@echo "Running documentation generation for path: ${path}..."
	@${API_CLIENT} docs "${path}"

analyze: ## Analyze a specific file. Usage: make analyze file="/project/src/main.py".
	@echo "Running code analysis for file: ${file}..."
	@${API_CLIENT} analyze "${file}"

# --- Help Command ---
.PHONY: help
help: ## Show this help message.
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
