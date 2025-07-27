# scripts/api_client.py
import argparse
import requests
import json
import sys

# Defines the base URL for our API server
API_BASE_URL = "http://localhost:8000"

def execute_task_request(task_name: str, data: dict, model: str | None):
    """Generic function to call the /tasks/{task_name} endpoint."""
    url = f"{API_BASE_URL}/tasks/{task_name}"
    payload = {"data": data}
    if model:
        payload["model"] = model
    
    try:
        # Set a long timeout for potentially long-running AI tasks (e.g., agents)
        response = requests.post(url, json=payload, timeout=600) # 10 minute timeout
        
        # Raise an exception for bad HTTP status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Pretty-print the JSON response from the server
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the command-line client."""
    parser = argparse.ArgumentParser(
        description="API Client for the AI Assistant. Called by the Makefile."
    )
    
    # This client is designed to be simple, taking the task name and a JSON string of data
    parser.add_argument("task_name", help="Name of the task to run (e.g., planning, docs).")
    parser.add_argument("json_data", help="JSON string with the data for the task (e.g., '{\"description\": \"...\"}').")
    parser.add_argument("--model", help="(Optional) Override the default model. Ex: OPENAI:gpt-4o")
    
    args = parser.parse_args()
    
    try:
        # Validate that the data string is valid JSON
        data_dict = json.loads(args.json_data)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data provided.", file=sys.stderr)
        sys.exit(1)
        
    execute_task_request(args.task_name, data_dict, args.model)

if __name__ == "__main__":
    main()
