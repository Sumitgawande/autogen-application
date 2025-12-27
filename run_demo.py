import requests

with open("examples/buggy_code.py") as f:
    code = f.read()

response = requests.post(
    "http://localhost:8000/debug",
    json={"code": code}
)

print(response.json())
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