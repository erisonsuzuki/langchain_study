# LangChain Study Project

This project is a command-line application created to study and demonstrate the core concepts of the LangChain framework. It shows how to build a simple application with LangChain, including how to switch between different Large Language Model (LLM) providers like OpenAI, Google, and Ollama.

## Features

*   **Multiple LLM Providers**: Easily switch between OpenAI (GPT-3.5 Turbo), Google (Gemini 1.5 Pro), and a local Ollama instance (Llama 3).
*   **Simple and Extensible**: The project structure is straightforward, making it easy to understand, extend, and experiment with different chains and prompts.
*   **Command-Line Interface**: Run the application directly from your terminal.
*   **Environment-Based Configuration**: API keys are managed securely using a `.env` file.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

*   Python 3.8 or higher
*   Access to OpenAI or Google API keys, or a running Ollama instance.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root of the project directory:
    ```bash
    touch .env
    ```

2.  Add your API keys to the `.env` file. You only need to add the keys for the providers you intend to use.

    ```env
    OPENAI_API_KEY="your_openai_api_key"
    GOOGLE_API_KEY="your_google_api_key"
    ```

    *Note: For Ollama, no API key is required as it runs locally.*

## Usage

To run the application, use the following command, specifying the desired model provider (`openai`, `google`, or `ollama`):

```bash
python -m app.main <provider>
```

### Examples

**Using OpenAI:**
```bash
python -m app.main openai
```

**Using Google:**
```bash
python -m app.main google
```

**Using Ollama:**
*Ensure your local Ollama instance is running before executing the command.*
```bash
python -m app.main ollama
```

## Docs

These records provide context and reasoning, serving as a learning history for the project.

You can find the docs [`here`](docs).
