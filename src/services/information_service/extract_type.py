import xml.etree.ElementTree as ET

def extract_activity_type(gpx_file):
    tree = ET.parse(gpx_file)
    root = tree.getroot()

    namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

    activity_type = root.find(".//gpx:trk/gpx:type", namespace)

    if activity_type is None:
        return None

    return activity_type.text


