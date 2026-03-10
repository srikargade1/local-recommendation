import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import requests

load_dotenv()

FSQ_API_KEY = os.environ.get("FOURSQUARE_API_KEY")
FSQ_API_URL = os.environ.get("FSQ_API_URL", "https://api.foursquare.com/v3/places/search")
FSQ_PHOTOS_URL = "https://api.foursquare.com/v3/places/{fsq_id}/photos"

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
        "radius": radius_meters,
        "fields": "fsq_id,name,location,distance,categories,chains,geocodes,closed_bucket,hours,popularity,rating,price"
    }

    if input_data.get("open_now"):
        params["open_now"] = "true"

    if "max_price" in input_data:
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


def _fetch_photo_for_place(fsq_id):
    """Fetches the first available photo URL for a given place ID."""
    try:
        url = FSQ_PHOTOS_URL.format(fsq_id=fsq_id)
        response = requests.get(url, headers=HEADERS, params={"limit": 1}, timeout=5)
        if response.status_code == 200:
            photos = response.json()
            if photos:
                p = photos[0]
                return fsq_id, f"{p['prefix']}300x200{p['suffix']}"
    except Exception as e:
        print(f"⚠️ Photo fetch failed for {fsq_id}: {e}")
    return fsq_id, None


def format_places(raw_places):
    """
    Converts raw Foursquare API results into a clean internal schema.
    Note: chain filtering is intentionally left to the pipeline's filter step
    so the user's exclude_chains preference is respected.
    """
    results = []

    for place in raw_places:
        is_chain = bool(place.get("chains"))
        coords = place.get("geocodes", {}).get("main", {})
        categories = [c["name"] for c in place.get("categories", [])]

        # closed_bucket is more reliable than parsing hours strings.
        # Values: "VeryLikelyOpen", "LikelyOpen", "Unsure", "LikelyClosed", "VeryLikelyClosed"
        closed_bucket = place.get("closed_bucket", "Unsure")
        is_open_now = closed_bucket in ("VeryLikelyOpen", "LikelyOpen")

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
            "map_link": f"https://maps.google.com/?q={coords.get('latitude')},{coords.get('longitude')}",
            "is_open_now": is_open_now,
            "closed_bucket": closed_bucket,
            "rating": place.get("rating"),
            "popularity": place.get("popularity"),
            "price": place.get("price"),
            "photo_url": None,  # populated by enrich_with_photos
        }
        results.append(formatted)

    return results


def enrich_with_photos(places):
    """
    Fetches one photo per place in parallel using threads.
    Falls back gracefully — places without photos just have photo_url = None.
    """
    fsq_ids = [p["fsq_id"] for p in places]

    photo_map = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(_fetch_photo_for_place, fsq_id): fsq_id for fsq_id in fsq_ids}
        for future in as_completed(futures):
            fsq_id, photo_url = future.result()
            photo_map[fsq_id] = photo_url

    for place in places:
        place["photo_url"] = photo_map.get(place["fsq_id"])

    return places
