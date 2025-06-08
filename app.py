from flask import Flask, request, jsonify
from core.pipeline import run_pipeline

app = Flask(__name__)

@app.route("/places", methods=["POST"])
def get_places():
    data = request.json

    # Required inputs
    user_prompt = data.get("prompt")
    user_lat = data.get("lat")
    user_lon = data.get("lon")
    gmaps_key = data.get("gmaps_api_key")

    # Validate required fields
    if not all([user_prompt, user_lat, user_lon, gmaps_key]):
        return jsonify({
            "error": "Missing required fields: 'prompt', 'lat', 'lon', or 'gmaps_api_key'"
        }), 400

    try:
        results = run_pipeline(user_prompt, user_lat, user_lon, gmaps_key)
        return jsonify(results)
    except Exception as e:
        print("❌ Pipeline error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
