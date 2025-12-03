#!/usr/bin/env python3
"""
Pattern-brained vs Simple: A quick experiment to see what happens when you
ask an LLM to use design patterns liberally vs write the simplest code possible.
"""

import anthropic
import json
from pathlib import Path
from datetime import datetime

client = anthropic.Anthropic()

SYSTEM_PATTERN_BRAINED = """You are an expert software engineer who believes strongly in
design patterns and proper software architecture. When writing code, you should:
- Use established design patterns (Factory, Strategy, Observer, Singleton, etc.) where applicable
- Create proper abstractions, interfaces, and base classes
- Separate concerns into distinct classes and modules
- Follow SOLID principles rigorously
- Think about extensibility and maintainability
- Use dependency injection where appropriate

Write production-quality, well-architected code."""

SYSTEM_SIMPLE = """You are a pragmatic software engineer who values simplicity above all.
When writing code, you should:
- Write the most direct, straightforward solution possible
- Avoid abstractions unless absolutely necessary
- Prefer functions over classes when possible
- Minimize the number of files, classes, and indirection
- If it can be done in 10 lines, don't write 100
- YAGNI (You Aren't Gonna Need It) - don't build for hypothetical futures

Write the simplest code that works."""

PROBLEMS = [
    {
        "id": "fizzbuzz",
        "name": "FizzBuzz",
        "prompt": "Write a function that prints numbers from 1 to 100. For multiples of 3, print 'Fizz'. For multiples of 5, print 'Buzz'. For multiples of both, print 'FizzBuzz'."
    },
    {
        "id": "reverse_string",
        "name": "Reverse String",
        "prompt": "Write a function that reverses a string."
    },
    {
        "id": "fibonacci",
        "name": "Fibonacci",
        "prompt": "Write a function that returns the nth Fibonacci number."
    },
    {
        "id": "palindrome",
        "name": "Palindrome Checker",
        "prompt": "Write a function that checks if a string is a palindrome."
    },
    {
        "id": "todo_list",
        "name": "Todo List",
        "prompt": "Write a simple todo list application with add, remove, and list functionality."
    },
    {
        "id": "calculator",
        "name": "Calculator",
        "prompt": "Write a calculator that supports add, subtract, multiply, and divide operations."
    },
    {
        "id": "user_validator",
        "name": "User Validator",
        "prompt": "Write code to validate user registration data: email must be valid format, password must be at least 8 characters with a number, username must be alphanumeric."
    },
    {
        "id": "file_processor",
        "name": "File Processor",
        "prompt": "Write code that reads a CSV file and outputs JSON with the same data."
    },
    {
        "id": "rate_limiter",
        "name": "Rate Limiter",
        "prompt": "Write a rate limiter that allows max N requests per minute for a given user ID."
    },
    {
        "id": "shopping_cart",
        "name": "Shopping Cart",
        "prompt": "Write a shopping cart that can add items, remove items, apply discount codes, and calculate totals."
    },
]


def run_problem(problem: dict, system_prompt: str, style_name: str) -> dict:
    """Run a single problem with a given system prompt."""
    print(f"  Running {problem['name']} ({style_name})...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": problem["prompt"] + "\n\nPlease write this in Python."}
        ]
    )

    content = response.content[0].text
    tokens_out = response.usage.output_tokens

    return {
        "problem_id": problem["id"],
        "problem_name": problem["name"],
        "prompt": problem["prompt"],
        "style": style_name,
        "response": content,
        "output_tokens": tokens_out,
    }


def main():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []

    print("Running pattern-brained vs simple comparison...\n")

    for problem in PROBLEMS:
        print(f"Problem: {problem['name']}")

        # Run both styles
        pattern_result = run_problem(problem, SYSTEM_PATTERN_BRAINED, "pattern_brained")
        simple_result = run_problem(problem, SYSTEM_SIMPLE, "simple")

        results.append(pattern_result)
        results.append(simple_result)

        # Save individual outputs for easy reading
        problem_dir = output_dir / problem["id"]
        problem_dir.mkdir(exist_ok=True)

        (problem_dir / "pattern_brained.py.md").write_text(
            f"# {problem['name']} - Pattern Brained\n\n"
            f"**Prompt:** {problem['prompt']}\n\n"
            f"**Output tokens:** {pattern_result['output_tokens']}\n\n"
            f"## Response\n\n{pattern_result['response']}"
        )

        (problem_dir / "simple.py.md").write_text(
            f"# {problem['name']} - Simple\n\n"
            f"**Prompt:** {problem['prompt']}\n\n"
            f"**Output tokens:** {simple_result['output_tokens']}\n\n"
            f"## Response\n\n{simple_result['response']}"
        )

        print(f"  Pattern: {pattern_result['output_tokens']} tokens, Simple: {simple_result['output_tokens']} tokens")
        print()

    # Save full results
    results_file = output_dir / f"results_{timestamp}.json"
    results_file.write_text(json.dumps(results, indent=2))

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    pattern_tokens = sum(r["output_tokens"] for r in results if r["style"] == "pattern_brained")
    simple_tokens = sum(r["output_tokens"] for r in results if r["style"] == "simple")

    print(f"Total pattern-brained tokens: {pattern_tokens}")
    print(f"Total simple tokens: {simple_tokens}")
    print(f"Ratio: {pattern_tokens / simple_tokens:.2f}x")
    print()
    print(f"Results saved to {output_dir}/")
    print(f"Full JSON: {results_file}")


if __name__ == "__main__":
    main()
