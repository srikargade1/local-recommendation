def filter_places(
    places,
    max_walk_minutes=None,
    max_drive_minutes=None,
    exclude_chains=False,
    must_be_open=False
):
    filtered = []

    excluded = {
        "chains": 0,
        "walk_time": 0,
        "drive_time": 0,
        "not_open": 0
    }

    if max_walk_minutes is not None:
        max_walk_minutes = float(max_walk_minutes)
    if max_drive_minutes is not None:
        max_drive_minutes = float(max_drive_minutes)

    for place in places:
        if exclude_chains and place.get("is_chain", False):
            excluded["chains"] += 1
            continue

        walk_seconds = place.get("travel_info", {}).get("walking", {}).get("duration_value")
        walk_time = walk_seconds / 60 if walk_seconds is not None else float("inf")

        if max_walk_minutes is not None and walk_time > max_walk_minutes:
            excluded["walk_time"] += 1
            continue

        drive_seconds = place.get("travel_info", {}).get("driving", {}).get("duration_value")
        drive_time = drive_seconds / 60 if drive_seconds is not None else float("inf")

        if max_drive_minutes is not None and drive_time > max_drive_minutes:
            excluded["drive_time"] += 1
            continue

        # Use Foursquare's closed_bucket signal instead of parsing a display string.
        # is_open_now is set in format_places based on closed_bucket values.
        if must_be_open and not place.get("is_open_now", False):
            excluded["not_open"] += 1
            continue

        filtered.append(place)

    print(f"🔍 Filtered out: {excluded}")
    return filtered
