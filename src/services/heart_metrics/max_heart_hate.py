def calculate_max_heart_rate(points):

    hrs = [
        p["heart_rate"]
        for p in points
        if p["heart_rate"] is not None
    ]

    if not hrs:
        return None

    return max(hrs)