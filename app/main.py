from dotenv import load_dotenv
load_dotenv()  # loads .env into environment
from fastapi import FastAPI
from pydantic import BaseModel
from app import self_heal

app = FastAPI(title="Autonomous Self-Debugging Agent")

class DebugRequest(BaseModel):
    code: str

class DebugResponse(BaseModel):
    fixed_code: str
    success: bool
    attempts: int
    error: str

@app.post("/debug", response_model=DebugResponse)
def debug(request: DebugRequest):
    result = self_heal(request.code, max_attempts=3)

    return DebugResponse(
        fixed_code=result["fixed_code"],
        success=result["success"],
        attempts=result["attempts"],
        error=result["error"]
    )
