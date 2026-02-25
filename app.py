from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://veo-google-free.freegen.workers.dev"

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": BASE_URL,
    "referer": BASE_URL + "/",
    "user-agent": "Mozilla/5.0"
}

# ----------------------------
# Home
# ----------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "usage": {
            "/gen?prompt=your_text": "Generate task",
            "/api/status/<task_id>": "Check task status"
        }
    })

# ----------------------------
# Generate via GET
# Example: /gen?prompt=A cat flying
# ----------------------------
@app.route("/gen", methods=["GET"])
def generate():
    prompt = request.args.get("prompt")

    if not prompt:
        return jsonify({"error": "prompt parameter required"}), 400

    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            headers=HEADERS,
            json={"prompt": prompt},
            timeout=60
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Status
# ----------------------------
@app.route("/api/status/<task_id>", methods=["GET"])
def status(task_id):
    try:
        response = requests.get(
            f"{BASE_URL}/api/status/{task_id}",
            headers=HEADERS,
            timeout=30
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)