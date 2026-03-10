import requests
import os

GOOGLE_DISTANCE_MATRIX_URL = os.environ.get(
    "GOOGLE_DISTANCE_MATRIX_URL",
    "https://maps.googleapis.com/maps/api/distancematrix/json"
)


def enrich_with_travel_times(places, origin_lat, origin_lon, api_key):
    """
    Enriches each place with travel time and distance for walking, driving, and transit.
    Uses batched requests — one API call per mode instead of one per place per mode.
    For 20 places this reduces API calls from 60 down to 3.
    """
    if not places or not api_key:
        return places

    modes = ["walking", "driving", "transit"]

    # Build a pipe-separated list of all destinations in one string
    destinations = "|".join(
        f"{p['coordinates']['lat']},{p['coordinates']['lon']}" for p in places
    )

    for mode in modes:
        params = {
            "origins": f"{origin_lat},{origin_lon}",
            "destinations": destinations,
            "mode": mode,
            "units": "metric",
            "key": api_key
        }
        try:
            response = requests.get(GOOGLE_DISTANCE_MATRIX_URL, params=params)
            elements = response.json()["rows"][0]["elements"]

            for place, element in zip(places, elements):
                place.setdefault("travel_info", {})[mode] = {
                    "duration_text": element.get("duration", {}).get("text"),
                    "duration_value": element.get("duration", {}).get("value"),
                    "distance_text": element.get("distance", {}).get("text"),
                    "distance_value": element.get("distance", {}).get("value"),
                }
        except Exception as e:
            print(f"⚠️ Batched travel info failed for mode {mode}: {e}")
            for place in places:
                place.setdefault("travel_info", {})[mode] = {
                    "duration_text": None,
                    "duration_value": None,
                    "distance_text": None,
                    "distance_value": None,
                }

    return places


def add_direction_links(places, user_lat, user_lon, mode="walking"):
    for p in places:
        dest = f"{p['coordinates']['lat']},{p['coordinates']['lon']}"
        origin = f"{user_lat},{user_lon}"
        link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}&travelmode={mode}"
        p["directions_link"] = link
    return places
