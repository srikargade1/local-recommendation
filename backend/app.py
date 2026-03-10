import json
import os
from flask import Flask, request, jsonify
from core.pipeline import run_pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://frontend-r0o4.onrender.com"])

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback_log.json")


@app.route("/places", methods=["POST"])
def get_places():
    data = request.json
    print("🔍 Request body:", data)

    user_prompt = data.get("prompt")
    user_lat = data.get("lat")
    user_lon = data.get("lon")
    gmaps_key = data.get("gmaps_api_key")
    radius_meters = data.get("radius_meters", 1000)
    max_walk_minutes = data.get("max_walk_minutes")
    max_drive_minutes = data.get("max_drive_minutes")
    exclude_chains = data.get("exclude_chains", False)
    must_be_open = data.get("must_be_open", False)
    conversation_history = data.get("conversation_history", [])

    if not all([user_prompt, user_lat, user_lon, gmaps_key]):
        return jsonify({
            "error": "Missing required fields: 'prompt', 'lat', 'lon', or 'gmaps_api_key'"
        }), 400

    try:
        results = run_pipeline(
            user_prompt, user_lat, user_lon, gmaps_key,
            max_walk_minutes, max_drive_minutes, exclude_chains,
            must_be_open, radius_meters,
            conversation_history=conversation_history
        )
        return jsonify(results)
    except Exception as e:
        print("❌ Pipeline error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/feedback", methods=["POST"])
def save_feedback():
    """
    Stores thumbs-up/down signals per place per query.
    Collected data can later be used to tune scoring weights.
    """
    data = request.json
    entry = {
        "fsq_id": data.get("fsq_id"),
        "place_name": data.get("place_name"),
        "query": data.get("query"),
        "thumbs_up": data.get("thumbs_up"),
    }

    feedback = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                feedback = json.load(f)
        except (json.JSONDecodeError, IOError):
            feedback = []

    feedback.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f, indent=2)

    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True)
