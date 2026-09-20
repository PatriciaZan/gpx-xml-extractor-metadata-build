from src.services.metrics import haversine

# Distances (in km) to find best efforts for
BEST_EFFORT_DISTANCES_KM = [5.0]


def find_best_effort(points: list[dict], target_km: float) -> dict | None:
    """
    Finds the fastest segment of exactly `target_km` distance
    using a two-pointer sliding window over GPS points.

    Returns a dict with metrics for the best segment, or None
    if the activity is shorter than target_km.
    """
    n = len(points)
    if n < 2:
        return None

    # Precompute cumulative distances between consecutive points
    # so we can cheaply sum any window [i, j]
    seg_distances = []
    for i in range(1, n):
        d = haversine(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"],     points[i]["lon"],
        )
        seg_distances.append(d)
    # seg_distances[i] = distance from points[i] to points[i+1]

    best = None
    best_speed = -1.0

    left = 0
    window_km = 0.0

    for right in range(1, n):
        # Expand window to the right
        window_km += seg_distances[right - 1]

        # Shrink from the left until we're just at or above target
        while window_km - seg_distances[left] >= target_km and left < right - 1:
            window_km -= seg_distances[left]
            left += 1

        if window_km < target_km:
            continue

        # We have a window [left, right] covering >= target_km
        t_start = points[left]["time"]
        t_end   = points[right]["time"]

        if t_start is None or t_end is None:
            continue

        elapsed_sec = (t_end - t_start).total_seconds()
        if elapsed_sec <= 0:
            continue

        avg_speed = round(window_km / (elapsed_sec / 3600), 2)

        if avg_speed > best_speed:
            best_speed = avg_speed
            segment_points = points[left: right + 1]

            best = {
                "distance_km":  round(window_km, 2),
                "elapsed_sec":  int(elapsed_sec),
                "avg_speed_kmh": avg_speed,
                "avg_hr":       _avg(segment_points, "heart_rate"),
                "avg_power_w":  _avg(segment_points, "power"),
            }

    return best


def calculate_best_efforts(points: list[dict]) -> dict:
    """
    Returns best efforts for all configured distances.
    Keys are human-readable strings like "5km".
    """
    results = {}
    for distance in BEST_EFFORT_DISTANCES_KM:
        label = f"{int(distance)}km" if distance == int(distance) else f"{distance}km"
        results[label] = find_best_effort(points, distance)
    return results


def _avg(points: list[dict], field: str) -> float | None:
    """Average of a numeric field across points, ignoring None values."""
    values = [p[field] for p in points if p.get(field) is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 1)
