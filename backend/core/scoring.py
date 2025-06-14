DEFAULT_WEIGHTS = {
    "distance": -1 / 20,
    "chain_penalty": -200,
    "match_bonus": 50,
    "rating_bonus": 20
}

def score_place(place, parsed_filters, user_query, weights=None):
    if weights is None:
        weights = DEFAULT_WEIGHTS

    score = 0

    distance = place.get("distance_meters", 10000)
    score += weights["distance"] * distance

    if place.get("is_chain"):
        score += weights["chain_penalty"]

    categories = [cat.lower() for cat in place.get("categories", [])]
    query_words = user_query.lower().split()
    match_score = sum(1 for word in query_words if any(word in cat for cat in categories))
    score += weights["match_bonus"] * match_score

    if "rating" in place:
        score += weights["rating_bonus"] * place["rating"]

    return round(score, 2)


def score_and_sort_places(places, parsed_filters, user_query):
    for place in places:
        place["score"] = score_place(place, parsed_filters, user_query)
    return sorted(places, key=lambda x: x["score"], reverse=True)
