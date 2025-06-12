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

    for place in places:
        if exclude_chains and place.get("is_chain", False):
            excluded["chains"] += 1
            continue

        walk_info = place.get("travel_info", {}).get("walking", {})
        walk_seconds = walk_info.get("duration_value")
        walk_time = walk_seconds / 60 if walk_seconds is not None else float('inf')

        if max_walk_minutes is not None and walk_time > max_walk_minutes:
            excluded["walk_time"] += 1
            continue

        drive_info = place.get("travel_info", {}).get("driving", {})
        drive_seconds = drive_info.get("duration_value")
        drive_time = drive_seconds / 60 if drive_seconds is not None else float('inf')

        if max_drive_minutes is not None and drive_time > max_drive_minutes:
            excluded["drive_time"] += 1
            continue

        if must_be_open:
            hours = place.get("hours_display")
            if not hours or "open" not in hours.lower():
                excluded["not_open"] += 1
                continue

        filtered.append(place)

    print(f"🔍 Filtered out: {excluded}")
    return filtered
