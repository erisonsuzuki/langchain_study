# AI Assistant Architecture Guide

This document outlines the internal software architecture of the AI Developer Assistant. The design prioritizes maintainability, scalability, and testability by adhering to the SOLID principles and other Python best practices.

## Core Architectural Layers

The application is logically divided into three distinct layers:

1.  **API Layer (`api_main.py`):** The outermost layer, responsible for handling HTTP requests and responses. It acts as a thin "controller," delegating all business logic to the Service Layer. It uses FastAPI's Dependency Injection system to acquire services.

2.  **Service Layer (`services/`):** The heart of the application. Each service encapsulates the complete business logic for a single task (e.g., planning a feature, generating documentation). This layer is responsible for coordinating with the configuration module to get prompts and settings, and with the LLM factory to get a language model instance.

3.  **Configuration Layer (`config/`):** This layer is responsible for all external configuration. It loads settings from `.env` files, YAML files (`llm_settings.yaml`), and prompt files (`prompts/*.md`), providing a centralized point of access for the rest of the application.

## Application of SOLID Principles

The SOLID principles were the primary guide for this refactoring.

### S - Single Responsibility Principle (SRP)

* **Principle:** A class or module should have only one reason to change.
* **Application in this Project:**
    * The **API Layer** (`api_main.py`) is now only responsible for web concerns (parsing requests, returning JSON responses, handling HTTP errors). It no longer contains any business logic.
    * Each class in the **Service Layer** (e.g., `PlanningService`) is responsible for a single, complete business task. If the logic for planning a feature changes, only `PlanningService` needs to be modified.
    * The **Configuration Layer** (`config/settings.py`) is solely responsible for loading and providing configuration data.

### O - Open/Closed Principle

* **Principle:** Software entities should be open for extension but closed for modification.
* **Application in this Project:**
    * The introduction of the Service Layer makes the system highly extensible. To add a new capability (e.g., a "Summarizer"), we can simply add a new `summarizer_service.py` file and a new endpoint in `api_main.py`. The existing, proven services like `PlanningService` do not need to be modified.

### L - Liskov Substitution Principle

* **Principle:** Subtypes must be substitutable for their base types.
* **Application in this Project:**
    * This is perfectly demonstrated by LangChain's `BaseChatModel`. Our LLM Factory (`get_llm_instance`) returns various concrete types (`ChatOllama`, `ChatOpenAI`, etc.), but the Service Layer treats them all generically as `BaseChatModel` instances, calling the same methods on them (e.g., `.invoke()`).

### I - Interface Segregation Principle

* **Principle:** Clients should not be forced to depend on interfaces they do not use.
* **Application in this Project:**
    * We've introduced `services/base_service.py` with an `AbstractTaskService`. While simple, it defines a clear and minimal contract (`execute` method) that all services adhere to. This ensures a consistent interface for any service we create.

### D - Dependency Inversion Principle

* **Principle:** High-level modules should not depend on low-level modules; both should depend on abstractions.
* **Application in this Project:**
    * This is achieved through **Dependency Injection**. The high-level API Layer (`api_main.py`) does not directly instantiate concrete service classes. Instead, it declares a dependency (e.g., `service: PlanningService = Depends()`), and the FastAPI framework is responsible for "injecting" a valid instance. This decouples the web layer from the business logic layer.

## Other Best Practices

* **Structured Logging:** The project should be further improved by replacing `print()` statements with Python's `logging` module for structured, leveled logging.
* **Centralized Error Handling:** FastAPI's exception handlers can be used to catch custom exceptions from the Service Layer and translate them into meaningful HTTP error responses.
* **Testability:** The Service Layer is now highly testable. Unit tests can be written for each service by "mocking" the `get_llm_instance` call, allowing verification of the service's logic in complete isolation from any actual LLM.
