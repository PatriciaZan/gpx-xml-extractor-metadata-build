
from src.services.parsers.gpx_points import extract_track_points


def calculate_heart_metrics(root):
    points = extract_track_points(root)
    heart_rates = [
        point["heart_rate"]
        for point in points
        if point["heart_rate"] is not None
    ]

    if not heart_rates:
        return {
            "average": None,
            "maximum": None,
            "minimum": None,
        }

    return {
        "average": round(sum(heart_rates) / len(heart_rates)),
        "maximum": max(heart_rates),
        "minimum": min(heart_rates),
    }


#def calculate_heart_metrics2(root):
#    points = extract_track_points(root)
#    result = calculate_heart_rate_metrics(points)
#    print(result)


#def calculate_heart_rate_metrics(points: list[dict]) -> dict:
