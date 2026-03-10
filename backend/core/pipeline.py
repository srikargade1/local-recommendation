from core.llm_parser import parse_prompt_to_filters, rerank_with_explanation
from core.fsq_api import build_query_params, fetch_places, format_places, enrich_with_photos
from core.maps import enrich_with_travel_times, add_direction_links
from core.filters import filter_places
from core.scoring import score_and_sort_places

# Only re-rank the top N candidates to keep LLM costs low
RERANK_TOP_N = 10


def run_pipeline(
    user_prompt,
    user_lat,
    user_lon,
    gmaps_api_key,
    max_walk_minutes,
    max_drive_minutes,
    exclude_chains,
    must_be_open,
    radius_meters,
    conversation_history=None
):
    # 1. Parse prompt → structured filters + preferences
    #    Conversation history lets refinement queries ("something quieter") build on prior context
    parsed_filters = parse_prompt_to_filters(user_prompt, conversation_history=conversation_history)

    # 2. Build Foursquare query params
    query_params = build_query_params(parsed_filters, user_lat, user_lon, radius_meters)

    # 3. Fetch raw places from Foursquare
    raw_places = fetch_places(query_params)

    # 4. Format into clean internal schema (chain filtering happens in step 6)
    formatted = format_places(raw_places)

    # 5. Enrich with travel times (batched: 3 API calls instead of 3 x N)
    enriched = enrich_with_travel_times(formatted, user_lat, user_lon, api_key=gmaps_api_key)

    # 6. Filter by user constraints (walk time, drive time, chains, open status)
    filtered = filter_places(
        enriched,
        max_walk_minutes=max_walk_minutes,
        max_drive_minutes=max_drive_minutes,
        exclude_chains=exclude_chains,
        must_be_open=must_be_open
    )

    # 7. Initial score + sort using dynamic weights derived from LLM preferences
    scored = score_and_sort_places(filtered, parsed_filters, user_prompt)

    # 8. LLM re-ranks top candidates with full context + generates one-line explanations
    #    Falls back to scored order if re-ranking fails
    top = scored[:RERANK_TOP_N]
    rest = scored[RERANK_TOP_N:]
    reranked = rerank_with_explanation(top, user_prompt) + rest

    # 9. Fetch photos in parallel (graceful fallback if photos unavailable)
    with_photos = enrich_with_photos(reranked)

    # 10. Add Google Maps direction links
    final_results = add_direction_links(with_photos, user_lat, user_lon)

    return final_results
