# scripts/api_client.py
import argparse
import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def _make_request(endpoint: str, payload: dict):
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}", file=sys.stderr)
        sys.exit(1)

def handle_plan(args):
    payload = {"description": args.description}
    if args.model:
        payload["model"] = args.model
    _make_request("plan-feature", payload)

def handle_docs(args):
    payload = {"project_path": args.path}
    if args.model:
        payload["model"] = args.model
    _make_request("generate-docs", payload)

def main():
    parser = argparse.ArgumentParser(description="API Client for the AI Assistant.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_plan = subparsers.add_parser("plan", help="Create a technical plan for a new feature.")
    parser_plan.add_argument("description", help="Description of the feature to be planned.")
    parser_plan.add_argument("--model", help="(Optional) Override the default model. Ex: OPENAI:gpt-4o")
    parser_plan.set_defaults(func=handle_plan)

    parser_docs = subparsers.add_parser("docs", help="Generate documentation for a project.")
    parser_docs.add_argument("path", help="Path to the project INSIDE the container (e.g., /project/src).")
    parser_docs.add_argument("--model", help="(Optional) Override the default model.")
    parser_docs.set_defaults(func=handle_docs)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
