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
    return jsonify(env.state_manager.get_state())

# -----------------------------
# RESET ENDPOINT
# -----------------------------
@app.route("/reset", methods=["GET"])
def reset():
    task_level = request.args.get("task_level", "easy")
    state = env.reset(task_level)

    return jsonify({
        "message": f"Environment reset to {task_level}",
        "state": state
    })

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
    app.run(debug=True, port=8000)