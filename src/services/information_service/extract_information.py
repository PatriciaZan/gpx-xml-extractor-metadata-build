import xml.etree.ElementTree as ET
GPX_NAMESPACE = {"gpx": "http://www.topografix.com/GPX/1/1"}

def extract_activity_metadata(root: ET.Element) -> dict:
    if root is None:
        raise ValueError("GPX root element cannot be None")

    track = root.find(".//gpx:trk", GPX_NAMESPACE)

    if track is None:
        raise ValueError("GPX file does not contain a track")

    name = track.find("gpx:name", GPX_NAMESPACE)
    activity_type = track.find("gpx:type", GPX_NAMESPACE)

    return {
        "name": name.text.strip() if name is not None and name.text else None,
        "type": activity_type.text.strip() if activity_type is not None and activity_type.text else None,
    }