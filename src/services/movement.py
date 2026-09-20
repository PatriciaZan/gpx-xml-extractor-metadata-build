from src.services.metrics import haversine

# Minimum speed (km/h) to count as "moving" — filters GPS drift and real stops
MOVING_THRESHOLD_KMH = 3.0


def calculate_moving_time(points) -> int:
    moving_seconds = 0

    for i in range(1, len(points)):
        previous = points[i - 1]
        current = points[i]

        if previous["time"] is None or current["time"] is None:
            continue

        time_diff = (current["time"] - previous["time"]).total_seconds()
        if time_diff <= 0:
            continue

        distance = haversine(
            previous["lat"], previous["lon"],
            current["lat"],  current["lon"],
        )
        speed_kmh = distance / (time_diff / 3600)

        if speed_kmh > MOVING_THRESHOLD_KMH:
            moving_seconds += time_diff

    return int(moving_seconds)


def calculate_stopped_time(duration_sec, moving_time_sec) -> int:
    return max(0, duration_sec - moving_time_sec)
