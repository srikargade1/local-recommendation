from flask import Flask, request, jsonify
from core.pipeline import run_pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000",
                   "https://frontend-r0o4.onrender.com" ])


@app.route("/places", methods=["POST"])
def get_places():
    data = request.json
    print("🔍 Request body:", request.json)
    # Required inputs
    user_prompt = data.get("prompt")
    user_lat = data.get("lat")
    user_lon = data.get("lon")
    gmaps_key = data.get("gmaps_api_key")
    radius_meters = data.get("radius_meters", 1000)


    max_walk_minutes = data.get("max_walk_minutes")
    max_drive_minutes = data.get("max_drive_minutes")
    exclude_chains = data.get("exclude_chains", False)
    must_be_open = data.get("must_be_open", False)

    # Validate required fields
    if not all([user_prompt, user_lat, user_lon, gmaps_key]):
        return jsonify({
            "error": "Missing required fields: 'prompt', 'lat', 'lon', or 'gmaps_api_key'"
        }), 400

    try:
        results = run_pipeline(user_prompt, user_lat, user_lon, gmaps_key, max_walk_minutes, max_drive_minutes, exclude_chains, must_be_open, radius_meters)
        return jsonify(results)
    except Exception as e:
        print("❌ Pipeline error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
