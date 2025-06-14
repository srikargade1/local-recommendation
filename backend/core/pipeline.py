from core.llm_parser import parse_prompt_to_filters
from core.fsq_api import build_query_params, fetch_places, format_places
from core.maps import enrich_with_travel_times, add_direction_links
from core.filters import filter_places
from core.scoring import score_and_sort_places


def run_pipeline(user_prompt, user_lat, user_lon, gmaps_api_key, max_walk_minutes, max_drive_minutes, exclude_chains, must_be_open, radius_meters):
    # 1. Parse user prompt to filters
    parsed_filters = parse_prompt_to_filters(user_prompt)

    # 2. Build Foursquare query params
    query_params = build_query_params(parsed_filters, user_lat, user_lon, radius_meters)

    # 3. Fetch raw places
    raw_places = fetch_places(query_params)

    # 4. Format into usable internal schema
    formatted = format_places(raw_places)

    enriched = enrich_with_travel_times(formatted, user_lat, user_lon, api_key=gmaps_api_key)

    filtered = filter_places(enriched, max_walk_minutes=max_walk_minutes, max_drive_minutes=max_drive_minutes, exclude_chains=exclude_chains, must_be_open=must_be_open)

    # 6. Score and sort
    scored = score_and_sort_places(filtered, parsed_filters, user_prompt)

    # 7. Filter based on time/open criteria

    # 8. Add Google Maps direction links
    final_results = add_direction_links(scored, user_lat, user_lon)

    return final_results
