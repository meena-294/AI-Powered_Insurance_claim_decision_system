from flask import Flask, request, jsonify
from env.environment import HealthcareEnv
from models.action import ClaimAction

# ✅ GLOBAL ENV (VERY IMPORTANT)
env = HealthcareEnv()

app = Flask(__name__)

# -----------------------------------
# ROOT (optional)
# -----------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Healthcare Claim API is running 🚀"
    })


# -----------------------------------
# RESET (🔥 MUST BE POST)
# -----------------------------------
@app.route("/reset", methods=["POST"])
def reset():
    data = request.json or {}

    task_level = data.get("task_level", "medium")

    state = env.reset(task_level)

    return jsonify({
        "message": f"Environment reset to {task_level}",
        "state": state
    })


# -----------------------------------
# STATE (GET)
# -----------------------------------
@app.route("/state", methods=["GET"])
def get_state():
    state = env.state_manager.get_state()
    return jsonify(state)


# -----------------------------------
# STEP (POST)
# -----------------------------------
@app.route("/step", methods=["POST"])
def step():
    data = request.json or {}

    action_type = data.get("action_type")
    new_code = data.get("new_code")
    justification = data.get("justification")

    action = ClaimAction(
        action_type=action_type,
        new_code=new_code,
        justification=justification
    )

    state, reward, done, info = env.step(action)

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    })


# -----------------------------------
# RUN SERVER
# -----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
