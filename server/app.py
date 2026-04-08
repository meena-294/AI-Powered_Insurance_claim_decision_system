from flask import Flask, request, jsonify

# IMPORT YOUR ENV + AGENT
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

# ✅ GLOBAL INSTANCES (VERY IMPORTANT)
env = HealthcareEnv()
agent = RuleBasedAgent()

# CREATE APP
app = Flask(__name__)

# -----------------------------
# ROOT (TEST)
# -----------------------------
@app.route("/")
def home():
    return jsonify({"message": "Healthcare Claim API is running ✅"})

# -----------------------------
# STATE ENDPOINT
# -----------------------------
@app.route("/state", methods=["GET"])
def get_state():
    state = env.state_manager.get_state()

    if state is None:
        # auto initialize (VERY IMPORTANT for hackathon)
        state = env.reset("easy")

    return jsonify(state)
# -----------------------------
# RESET ENDPOINT
# -----------------------------
@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}

    task_level = data.get("task_level", "easy")

    state = env.reset(task_level)

 # debug

    return jsonify(state)

# -----------------------------
# STEP ENDPOINT
# -----------------------------
@app.route("/step", methods=["POST"])
def step():
    data = request.get_json()

    action = ClaimAction(
        action_type=data.get("action_type"),
        new_code=data.get("new_code"),
        justification=data.get("justification")
    )

    state, reward, done, info = env.step(action)

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    })

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
