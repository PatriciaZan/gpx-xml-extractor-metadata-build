from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2) -> float:
    """Returns distance in km between two lat/lon points."""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def calculate_distance(points) -> float:
    total = 0.0
    for i in range(1, len(points)):
        total += haversine(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"],     points[i]["lon"],
        )
    return round(total, 2)


def calculate_duration(points) -> int:
    start = points[0]["time"]
    end = points[-1]["time"]
    return int((end - start).total_seconds())


def calculate_elevation_gain(points) -> float:
    gain = 0.0
    for i in range(1, len(points)):
        prev_elev = points[i - 1]["elevation"]
        curr_elev = points[i]["elevation"]
        if prev_elev is None or curr_elev is None:
            continue
        diff = curr_elev - prev_elev
        if diff > 0:
            gain += diff
    return round(gain)


def calculate_elevation_loss(points) -> float:
    """Total meters descended across the ride."""
    loss = 0.0
    for i in range(1, len(points)):
        prev_elev = points[i - 1]["elevation"]
        curr_elev = points[i]["elevation"]
        if prev_elev is None or curr_elev is None:
            continue
        diff = curr_elev - prev_elev
        if diff < 0:
            loss += abs(diff)
    return round(loss)


def calculate_max_elevation(points) -> float | None:
    """Highest elevation point reached."""
    elevations = [p["elevation"] for p in points if p["elevation"] is not None]
    return round(max(elevations)) if elevations else None


def calculate_min_elevation(points) -> float | None:
    """Lowest elevation point reached."""
    elevations = [p["elevation"] for p in points if p["elevation"] is not None]
    return round(min(elevations)) if elevations else None


def calculate_max_speed(points) -> float:
    """Fastest point-to-point speed recorded (km/h)."""
    max_speed = 0.0
    for i in range(1, len(points)):
        if points[i - 1]["time"] is None or points[i]["time"] is None:
            continue
        time_diff = (points[i]["time"] - points[i - 1]["time"]).total_seconds()
        if time_diff <= 0:
            continue
        distance = haversine(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"],     points[i]["lon"],
        )
        speed = distance / (time_diff / 3600)
        if speed > max_speed:
            max_speed = speed
    return round(max_speed, 2)


def calculate_avg_speed(distance_km, duration_sec) -> float:
    if duration_sec <= 0:
        return 0.0
    hours = duration_sec / 3600
    return round(distance_km / hours, 2)