import requests
import os

GOOGLE_DISTANCE_MATRIX_URL = os.environ.get(
    "GOOGLE_DISTANCE_MATRIX_URL", 
    "https://maps.googleapis.com/maps/api/distancematrix/json"
)


def get_travel_info(origin_lat, origin_lon, dest_lat, dest_lon, mode="walking", api_key=None):
    """
    Fetches travel time and distance between origin and destination using the specified mode.
    Modes supported: 'walking', 'driving', 'transit', 'bicycling'
    """
    if api_key is None:
        return {
            "error": "API key is missing",
            "distance_text": None,
            "distance_value": None,
            "duration_text": None,
            "duration_value": None
        }

    params = {
        "origins": f"{origin_lat},{origin_lon}",
        "destinations": f"{dest_lat},{dest_lon}",
        "mode": mode,
        "units": "metric",
        "key": api_key
    }

    try:
        response = requests.get(GOOGLE_DISTANCE_MATRIX_URL, params=params)
        data = response.json()

        element = data["rows"][0]["elements"][0]
        if element.get("status") != "OK":
            return {
                "error": element.get("status"),
                "distance_text": None,
                "distance_value": None,
                "duration_text": None,
                "duration_value": None
            }

        return {
            "distance_text": element["distance"]["text"],
            "distance_value": element["distance"]["value"],
            "duration_text": element["duration"]["text"],
            "duration_value": element["duration"]["value"]
        }

    except Exception as e:
        return {
            "error": str(e),
            "distance_text": None,
            "distance_value": None,
            "duration_text": None,
            "duration_value": None
        }



def enrich_with_travel_times(places, origin_lat, origin_lon, api_key):
    """
    Enriches each place with travel time and distance for walking, driving, and transit.
    """
    modes = ["walking", "driving", "transit"]

    for place in places:
        place["travel_info"] = {}
        dest_lat = place["coordinates"]["lat"]
        dest_lon = place["coordinates"]["lon"]

        for mode in modes:
            try:
                travel_data = get_travel_info(origin_lat, origin_lon, dest_lat, dest_lon, mode=mode, api_key=api_key)
                place["travel_info"][mode] = travel_data
            except Exception as e:
                print(f"⚠️ Travel info failed for {place['name']} ({mode}): {e}")
                place["travel_info"][mode] = {
                    "error": str(e),
                    "distance_text": None,
                    "distance_value": None,
                    "duration_text": None,
                    "duration_value": None
                }

    return places



def add_direction_links(places, user_lat, user_lon, mode="walking"):
    for p in places:
        dest = f"{p['coordinates']['lat']},{p['coordinates']['lon']}"
        origin = f"{user_lat},{user_lon}"
        link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={dest}&travelmode={mode}"
        p["directions_link"] = link
    return places