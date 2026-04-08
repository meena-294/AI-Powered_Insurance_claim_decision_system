from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
 
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent
 
# ✅ GLOBAL INSTANCES
env = HealthcareEnv()
agent = RuleBasedAgent()
 
# CREATE APP
app = FastAPI()
 
 
# -----------------------------
# ROOT (TEST)
# -----------------------------
@app.get("/")
def home():
    return {"message": "Healthcare Claim API is running ✅"}
 
 
# -----------------------------
# RESET ENDPOINT
# ✅ Accepts task_level as QUERY PARAM → POST /reset?task_level=easy
# -----------------------------
@app.post("/reset")
def reset(task_level: str = "easy"):
    state = env.reset(task_level)
    return state
 
 
# -----------------------------
# STATE ENDPOINT
# -----------------------------
@app.get("/state")
def get_state():
    state = env.state_manager.get_state()
    return state
 
 
# -----------------------------
# STEP ENDPOINT
# -----------------------------
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
        "reward": reward,
        "done": done,
        "info": info
    }
 
 
# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
