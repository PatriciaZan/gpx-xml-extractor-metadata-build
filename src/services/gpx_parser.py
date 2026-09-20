import io
import gpxpy


def parse_gpx(content: bytes) -> list[dict]:
    """
    Parse a GPX file from raw bytes into a list of track points.
    Each point: { lat, lon, elevation, time, heart_rate }
    """
    gpx = gpxpy.parse(io.StringIO(content.decode("utf-8")))
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                heart_rate = _extract_heart_rate(point)

                power = _extract_field(point, "power")

                points.append({
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "elevation": point.elevation,
                    "time": point.time,
                    "heart_rate": heart_rate,
                    "power": power,
                })

    return points


def _extract_heart_rate(point) -> int | None:
    return _extract_field(point, "hr")


def _extract_field(point, tag_keyword: str) -> int | None:
    """
    Extracts a numeric value from GPX extensions by matching a keyword
    against the tag name (case-insensitive). Works for 'hr', 'power', etc.
    """
    try:
        for extension in point.extensions:
            for child in extension:
                if tag_keyword in child.tag.lower() and child.text:
                    return int(child.text)
    except Exception:
        pass
    return None
