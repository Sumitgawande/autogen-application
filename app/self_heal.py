from app.executor import run_code
from app.agent import debug_code

def self_heal(code: str, max_attempts: int = 3):
    last_error = ""

    for attempt in range(max_attempts):
        result = run_code(code)

        if result["returncode"] == 0:
            return {
                "fixed_code": code,
                "success": True,
                "attempts": attempt + 1,
                "error": ""
            }

        last_error = result["stderr"]
        code = debug_code(code, last_error)

    return {
        "fixed_code": code,
        "success": False,
        "attempts": max_attempts,
        "error": last_error
    }
