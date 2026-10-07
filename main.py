from pathlib import Path
import xml.etree.ElementTree as ET

from src.services.heart_metrics import average_heart_hate
from src.services.heart_metrics.heart_metrics import calculate_heart_metrics
from src.services.information_service.extract_information import extract_activity_metadata

PROJECT_ROOT = Path(__file__).parent
FILES_DIR = PROJECT_ROOT / "data"

def process_files():
    gpx_files = sorted(FILES_DIR.glob("*.gpx"))
    if not gpx_files:
        print("Nenhum arquivo .gpx encontrado em /data")
        return

    print(f"\nEncontrados {len(gpx_files)} arquivos GPX.\n")

    for gpx_file in gpx_files:
        tree = ET.parse(gpx_file)
        root = tree.getroot()

        information = extract_activity_metadata(root)
        print(information)

        average_heart_rate = calculate_heart_metrics(root)
        print(average_heart_rate)

process_files()