def calculate_avg_hr(points):

    hrs = [
        p["heart_rate"]
        for p in points
        if p["heart_rate"] is not None
    ]

    if not hrs:
        return None

    return round(
        sum(hrs) / len(hrs)
    )

def calculate_max_hr(points):

    hrs = [
        p["heart_rate"]
        for p in points
        if p["heart_rate"] is not None
    ]

    if not hrs:
        return None

    return max(hrs)

