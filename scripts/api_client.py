# scripts/api_client.py
import argparse
import requests
import json
import sys
import time

API_BASE_URL = "http://localhost:8000"

def _make_request(endpoint: str, payload: dict):
    """Helper function to make POST calls to the API."""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=payload, timeout=600) # 10 minute timeout
        response.raise_for_status()  # Raise an exception for 4xx/5xx http statuses
        
        # Pretty-print the JSON response
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}", file=sys.stderr)
        sys.exit(1)

def handle_plan(args):
    """Calls the /plan-feature endpoint."""
    payload = {"description": args.description}
    if args.model: payload["model"] = args.model
    _make_request("plan-feature", payload)

def handle_docs(args):
    """Calls the /generate-docs endpoint."""
    payload = {"project_path": args.path}
    if args.model: payload["model"] = args.model
    _make_request("generate-docs", payload)

def handle_analyze(args):
    """Calls the /analyze-code endpoint."""
    payload = {"file_path": args.file}
    if args.model: payload["model"] = args.model
    _make_request("analyze-code", payload)

def handle_edit(args):
    """Calls the /edit-code-agent endpoint."""
    payload = {"instruction": args.instruction}
    if args.model: payload["model"] = args.model
    _make_request("edit-code-agent", payload)

def handle_check_task(args):
    """Calls the /tasks/{task_id} endpoint."""
    url = f"{API_BASE_URL}/tasks/{args.task_id}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the command-line client."""
    parser = argparse.ArgumentParser(description="API Client for the AI Assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Plan Command
    parser_plan = subparsers.add_parser("plan", help="Create a technical plan for a new feature.")
    parser_plan.add_argument("description", help="Description of the feature.")
    parser_plan.add_argument("--model", help="Override the default model.")
    parser_plan.set_defaults(func=handle_plan)

    # Docs Command
    parser_docs = subparsers.add_parser("docs", help="Generate documentation.")
    parser_docs.add_argument("path", help="Path to the project inside the container.")
    parser_docs.add_argument("--model", help="Override the default model.")
    parser_docs.set_defaults(func=handle_docs)

    # Analyze Command
    parser_analyze = subparsers.add_parser("analyze", help="Analyze a code file.")
    parser_analyze.add_argument("file", help="Path to the file inside the container.")
    parser_analyze.add_argument("--model", help="Override the default model.")
    parser_analyze.set_defaults(func=handle_analyze)

    # Edit Command
    parser_edit = subparsers.add_parser("edit", help="Instruct the AI agent to edit code.")
    parser_edit.add_argument("instruction", help="High-level instruction for the code change.")
    parser_edit.add_argument("--model", help="Override the default agent model.")
    parser_edit.set_defaults(func=handle_edit)
    
    # Check Task Command
    parser_check = subparsers.add_parser("check_task", help="Check the status of a submitted task.")
    parser_check.add_argument("task_id", help="The ID of the task to check.")
    parser_check.set_defaults(func=handle_check_task)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
