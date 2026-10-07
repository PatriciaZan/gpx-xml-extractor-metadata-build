import xml.etree.ElementTree as ET

GPX_NAMESPACE = {
    "gpx": "http://www.topografix.com/GPX/1/1",
    "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
}


def extract_track_points(root: ET.Element) -> list[dict]:
    points = []

    track_points = root.findall(".//gpx:trkpt", GPX_NAMESPACE)

    for point in track_points:
        heart_rate = point.find(
            ".//gpxtpx:hr",
            GPX_NAMESPACE
        )

        elevation = point.find(
            "gpx:ele",
            GPX_NAMESPACE
        )

        timestamp = point.find(
            "gpx:time",
            GPX_NAMESPACE
        )

        points.append({
            "latitude": float(point.get("lat")),
            "longitude": float(point.get("lon")),
            "elevation": float(elevation.text) if elevation is not None else None,
            "time": timestamp.text if timestamp is not None else None,
            "heart_rate": int(heart_rate.text) if heart_rate is not None else None,
        })

    return points