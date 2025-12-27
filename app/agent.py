import os
from openai import OpenAI

MODEL = "anthropic/claude-3.5-sonnet"

SYSTEM_PROMPT = """
You are an expert Python debugging agent.
Your task:
1. Identify the exact root cause of the error
2. Apply the minimal fix required
3. Do not refactor or add features
4. Return ONLY the corrected full Python code
"""

def get_client():
    # Read the key at runtime, not import time
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    client = OpenAI(
        api_key=api_key,
        api_base="https://openrouter.ai/api/v1",
    )
    client._default_headers.update({
        "HTTP-Referer": "https://github.com/yourusername/self-debugging-agent",
        "X-Title": "Autonomous Self-Debugging Agent"
    })
    return client

def debug_code(code: str, error: str) -> str:
    client = get_client()  # create client at runtime
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Buggy Code:\n{code}\n\nError Trace:\n{error}"}
        ],
        temperature=0
    )

    fixed_code = response.choices[0].message.content.strip()

    # Remove triple backticks if present
    if "```" in fixed_code:
        parts = fixed_code.split("```")
        fixed_code = parts[2] if len(parts) > 2 else parts[1]

    return fixed_code
