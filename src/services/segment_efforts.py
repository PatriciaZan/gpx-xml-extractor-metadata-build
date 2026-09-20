from src.services.metrics import haversine

# Size of each segment in km
SEGMENT_SIZE_KM = 5.0


def calculate_segment_efforts(points: list[dict], segment_km: float = SEGMENT_SIZE_KM) -> list[dict]:
    """
    Splits the full ride into sequential segments of `segment_km` each.
    The last segment is included even if it's shorter than segment_km
    (e.g. a 23 km ride yields four 5 km segments + one ~3 km remainder).

    Returns a list of dicts, one per segment:
      {
        "segment":       "0-5km",
        "distance_km":   5.02,
        "elapsed_sec":   634,
        "avg_speed_kmh": 28.5,
        "avg_hr":        158,
        "avg_power_w":   null,
      }
    """
    if len(points) < 2:
        return []

    segments = []
    segment_index = 1          # which segment we're building (1-based)
    segment_start = 0          # index of the first point in current segment
    accumulated_km = 0.0       # distance covered so far in this segment
    segment_points = [points[0]]

    for i in range(1, len(points)):
        step_km = haversine(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"],     points[i]["lon"],
        )
        accumulated_km += step_km
        segment_points.append(points[i])

        if accumulated_km >= segment_km:
            # Close this segment
            seg = _build_segment(
                segment_points,
                segment_index,
                segment_km,
                accumulated_km,
            )
            if seg:
                segments.append(seg)

            # Start next segment from the current point
            segment_index += 1
            accumulated_km = 0.0
            segment_points = [points[i]]

    # Remainder segment (whatever distance is left after the last full segment)
    if len(segment_points) > 1 and accumulated_km > 0:
        seg = _build_segment(
            segment_points,
            segment_index,
            segment_km,
            accumulated_km,
        )
        if seg:
            segments.append(seg)

    return segments


def _build_segment(
    points: list[dict],
    index: int,
    segment_km: float,
    actual_km: float,
) -> dict | None:
    t_start = points[0]["time"]
    t_end   = points[-1]["time"]

    if t_start is None or t_end is None:
        return None

    elapsed_sec = (t_end - t_start).total_seconds()
    if elapsed_sec <= 0:
        return None

    start_km = (index - 1) * segment_km
    end_km   = start_km + actual_km

    label = f"{_fmt(start_km)}-{_fmt(end_km)}km"

    return {
        "segment":       label,
        "distance_km":   round(actual_km, 2),
        "elapsed_sec":   int(elapsed_sec),
        "avg_speed_kmh": round(actual_km / (elapsed_sec / 3600), 2),
        "avg_hr":        _avg(points, "heart_rate"),
        "avg_power_w":   _avg(points, "power"),
    }


def _fmt(km: float) -> str:
    """Format a km value: show as int if whole number, else 1 decimal."""
    return str(int(km)) if km == int(km) else f"{km:.1f}"


def _avg(points: list[dict], field: str) -> float | None:
    values = [p[field] for p in points if p.get(field) is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 1)
