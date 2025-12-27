from executor import run_code

def verify_fix(code: str):
    result = run_code(code)
    return result["returncode"] == 0
