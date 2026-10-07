def calculate_average_heart_rate(points: list[dict]) -> float | None:
    heart_rates = [
        points["heart_rate"]
        for points in points
        if points["heart_rate"] is not None
    ]

    if not heart_rates:
        return None

    return round(sum(heart_rates) / len(heart_rates))



