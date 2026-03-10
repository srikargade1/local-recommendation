import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def parse_prompt_to_filters(prompt, conversation_history=None):
    """
    Converts a natural language prompt into structured search filters.
    Accepts optional conversation_history (list of {role, content} dicts)
    so that refinement queries ("something quieter") are understood in context.

    Also extracts a 'preferences' object that the scoring layer uses to
    dynamically weight results — e.g. if the user cares about proximity,
    distance gets weighted more heavily.
    """
    system_msg = (
        "You are an assistant that converts user travel-related queries into JSON filter objects "
        "for place search. Only return the JSON object. Available fields are:\n"
        "- query (string): the core search term for Foursquare\n"
        "- open_now (boolean)\n"
        "- max_price (integer, 1-4)\n"
        "- exclude_chains (boolean)\n"
        "- radius_meters (integer, optional)\n"
        "- preferences (object) with these keys:\n"
        "  - prioritize_proximity (bool): user cares most about being close\n"
        "  - prioritize_uniqueness (bool): user wants local/indie spots over chains\n"
        "  - prioritize_quality (bool): user cares about ratings and reviews\n"
        "  - vibe_keywords (list of strings): atmosphere/mood words from the query\n"
        "Do not include any text outside the JSON."
    )

    messages = [{"role": "system", "content": system_msg}]

    # Include prior turns so refinement queries work in context
    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": f"User prompt: {prompt}"})

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    try:
        filters = json.loads(raw)
        print("🔍 Parsed filters:", filters)
        return filters
    except json.JSONDecodeError:
        print("❌ Failed to parse GPT response:", raw)
        return {
            "query": prompt,
            "open_now": False,
            "exclude_chains": False,
            "radius_meters": 1000,
            "preferences": {}
        }


def rerank_with_explanation(places, user_query):
    """
    Sends the top candidates to GPT for context-aware re-ranking.
    Returns the places in re-ranked order, each with an 'explanation' field
    describing why it was ranked where it was.

    This replaces the rigid hand-coded scoring as the final ranking step.
    The LLM can reason about nuance (e.g. 'cozy', 'quiet', 'romantic') that
    a weighted formula cannot.
    """
    if not places:
        return places

    place_summaries = []
    for i, place in enumerate(places):
        walk = place.get("travel_info", {}).get("walking", {}).get("duration_text", "unknown walk time")
        categories = ", ".join(place.get("categories", [])) or "unknown category"
        chain_label = "chain" if place.get("is_chain") else "local/independent"
        open_label = "open now" if place.get("is_open_now") else "open status unknown"
        rating = f"rated {place['rating']}/10" if place.get("rating") else "no rating"
        summary = (
            f"{i + 1}. {place['name']} | {categories} | {walk} walk | "
            f"{chain_label} | {open_label} | {rating}"
        )
        place_summaries.append(summary)

    places_text = "\n".join(place_summaries)

    system_msg = (
        "You are a local recommendation assistant. Given a user's query and a list of candidate places, "
        "rank them from best to worst match. Consider relevance to the query, "
        "vibe/atmosphere keywords, proximity, whether it is a local spot vs. chain, and open status. "
        "Return ONLY a JSON array where each object has: "
        "'rank' (1-indexed integer), 'original_index' (1-indexed from input list), "
        "'explanation' (one sentence explaining why this place fits the query). "
        "Do not include any text outside the JSON array."
    )

    user_msg = f'User query: "{user_query}"\n\nCandidates:\n{places_text}'

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()
        rankings = json.loads(raw)

        reranked = []
        for ranking in sorted(rankings, key=lambda x: x["rank"]):
            original_idx = ranking["original_index"] - 1
            if 0 <= original_idx < len(places):
                place = places[original_idx].copy()
                place["explanation"] = ranking.get("explanation", "")
                reranked.append(place)

        return reranked

    except Exception as e:
        print(f"⚠️ Re-ranking failed: {e} — returning original order")
        return places
