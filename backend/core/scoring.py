def build_weights(parsed_filters):
    """
    Dynamically adjusts scoring weights based on preferences extracted by the LLM.
    If the user said 'close to me' we weight distance heavily.
    If they said 'local spots only' we increase the chain penalty.
    If they said 'highly rated' we increase the rating bonus.
    """
    prefs = parsed_filters.get("preferences", {})
    return {
        "distance": -1 / 10 if prefs.get("prioritize_proximity") else -1 / 20,
        "chain_penalty": -300 if prefs.get("prioritize_uniqueness") else -200,
        "match_bonus": 50,
        "rating_bonus": 30 if prefs.get("prioritize_quality") else 20,
    }


def score_place(place, parsed_filters, user_query, weights=None):
    if weights is None:
        weights = build_weights(parsed_filters)

    score = 0

    distance = place.get("distance_meters", 10000)
    score += weights["distance"] * distance

    if place.get("is_chain"):
        score += weights["chain_penalty"]

    categories = [cat.lower() for cat in place.get("categories", [])]
    query_words = user_query.lower().split()
    match_score = sum(1 for word in query_words if any(word in cat for cat in categories))
    score += weights["match_bonus"] * match_score

    if place.get("rating"):
        score += weights["rating_bonus"] * place["rating"]

    # Boost confirmed-open places slightly
    if place.get("is_open_now"):
        score += 25

    return round(score, 2)


def score_and_sort_places(places, parsed_filters, user_query):
    weights = build_weights(parsed_filters)
    for place in places:
        place["score"] = score_place(place, parsed_filters, user_query, weights)
    return sorted(places, key=lambda x: x["score"], reverse=True)
