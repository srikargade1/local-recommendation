import os
from dotenv import load_dotenv
import requests

load_dotenv()  # Load .env file

FSQ_API_KEY = os.environ.get("FOURSQUARE_API_KEY")
FSQ_API_URL = os.environ.get("FSQ_API_URL", "https://api.foursquare.com/v3/places/search")

HEADERS = {
    "Authorization": FSQ_API_KEY,
    "accept": "application/json"
}

def build_query_params(input_data, lat, lon, radius_meters):
    params = {
        "ll": f"{lat},{lon}",
        "query": input_data.get("query", ""),
        "sort": "RELEVANCE",
        "limit": 20,
        "radius": radius_meters
    }

    if input_data.get("open_now"):
        params["open_now"] = "true"

    if "max_price" in input_data:
        # Foursquare expects a comma-separated list like 1,2
        max_p = input_data["max_price"]
        params["price"] = ",".join(str(i) for i in range(1, max_p + 1))

    return params


def fetch_places(params):
    response = requests.get(FSQ_API_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"❌ API Error {response.status_code}: {response.text}")
        return []

def format_places(raw_places, exclude_chains=True):
    results = []

    for place in raw_places:
        is_chain = bool(place.get("chains"))
        if exclude_chains and is_chain:
            continue

        coords = place.get("geocodes", {}).get("main", {})
        categories = [c["name"] for c in place.get("categories", [])]
        formatted = {
            "name": place["name"],
            "address": place["location"].get("formatted_address"),
            "distance_meters": place.get("distance"),
            "categories": categories,
            "is_chain": is_chain,
            "fsq_id": place["fsq_id"],
            "coordinates": {
                "lat": coords.get("latitude"),
                "lon": coords.get("longitude")
            },
            "map_link": f"https://maps.google.com/?q={coords.get('latitude')},{coords.get('longitude')}"
        }
        results.append(formatted)

    return results