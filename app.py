from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

# ✅ GLOBAL INSTANCES
env = HealthcareEnv()
agent = RuleBasedAgent()

app = FastAPI()

# --- ROOT & HEALTH CHECKS ---
@app.get("/")
def home():
    return {"status": "ok", "message": "Healthcare Claim API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- RESET ENDPOINT ---
# This version handles BOTH query parameters and JSON body payloads
@app.post("/reset")
async def reset(payload: Dict[str, Any] = Body(None), task_level: Optional[str] = None):
    """
    Handles:
    1. POST /reset?task_level=easy
    2. POST /reset with body {"task_level": "easy"}
    3. POST /reset with body {"difficulty": "easy"}
    """
    selected_level = "easy" # Default

    # Check JSON Body first (Standard for OpenEnv)
    if payload:
        selected_level = payload.get("task_level", payload.get("difficulty", "easy"))
    # Check Query Param second
    elif task_level:
        selected_level = task_level

    state = env.reset(selected_level)
    return state

# --- STATE ENDPOINT ---
@app.get("/state")
def get_state():
    # Ensuring we return a dictionary
    return env.state_manager.get_state()

# --- STEP ENDPOINT ---
class StepRequest(BaseModel):
    action_type: str
    new_code: Optional[str] = None
    justification: Optional[str] = None

@app.post("/step")
def step(request: StepRequest):
    action = ClaimAction(
        action_type=request.action_type,
        new_code=request.new_code,
        justification=request.justification
    )
    
    state, reward, done, info = env.step(action)
    
    return {
        "state": state,
        "reward": float(reward),
        "done": bool(done),
        "info": info
    }

# --- SERVER START ---
if __name__ == "__main__":
    # Standard OpenEnv port is 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
