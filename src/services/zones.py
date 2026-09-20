def create_zones(max_hr: int) -> dict:
    return {
        "z1": (0.50 * max_hr, 0.60 * max_hr),
        "z2": (0.60 * max_hr, 0.70 * max_hr),
        "z3": (0.70 * max_hr, 0.80 * max_hr),
        "z4": (0.80 * max_hr, 0.90 * max_hr),
        "z5": (0.90 * max_hr, 1.00 * max_hr),
    }


def calculate_zone_distribution(points, zones) -> dict:
    zone_counts = {"z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5": 0}

    for point in points:
        hr = point.get("heart_rate")
        if hr is None:
            continue
        for zone_name, (minimum, maximum) in zones.items():
            if minimum <= hr < maximum:
                zone_counts[zone_name] += 1
                break

    return zone_counts


def calculate_hr_zones_time(points, zones) -> dict:
    """
    Time in seconds spent in each HR zone.
    Uses the interval between consecutive points rather than point counts,
    so accuracy doesn't depend on GPS recording frequency.
    """
    zone_time = {"z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5": 0}

    for i in range(1, len(points)):
        prev = points[i - 1]
        curr = points[i]

        hr = prev.get("heart_rate")
        if hr is None:
            continue
        if prev["time"] is None or curr["time"] is None:
            continue

        interval_sec = (curr["time"] - prev["time"]).total_seconds()
        if interval_sec <= 0:
            continue

        for zone_name, (minimum, maximum) in zones.items():
            if minimum <= hr < maximum:
                zone_time[zone_name] += interval_sec
                break

    return {zone: int(secs) for zone, secs in zone_time.items()}


def zone_percentages(zone_counts) -> dict:
    total = sum(zone_counts.values())
    if total == 0:
        return {zone: 0.0 for zone in zone_counts}
    return {
        zone: round((count / total) * 100, 1)
        for zone, count in zone_counts.items()
    }