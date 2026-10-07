# FOR TESTING ONLY

import json
from pathlib import Path
from typing import Optional
from src.gpx_processor import process_gpx_file

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
FILES_DIR = PROJECT_ROOT / "files"
print(FILES_DIR)

user_max_hr = int(os.getenv("USER_MAX_HR"))
user_weight =  int(os.getenv("USER_WEIGHT"))
user_age = int(os.getenv("USER_AGE"))
user_gender = os.getenv("USER_GENDER")



def process_all_gpx_files(
    max_hr: int,
    user_weight: Optional[float] = None,
    user_age: Optional[float] = None,
    user_gender: Optional[str] = None,
):
    gpx_files = sorted(FILES_DIR.glob("*.gpx"))

    if not gpx_files:
        print("Nenhum arquivo .gpx encontrado em /files")
        return

    print(f"\nEncontrados {len(gpx_files)} arquivos GPX.\n")

    for gpx_file in gpx_files:
        print(f"Processando: {gpx_file.name}")
        try:
            with open(gpx_file, "rb") as file:
                content = file.read()
            result = process_gpx_file(
                content=content,
                max_hr=user_max_hr,
                user_weight=user_weight,
                user_age=user_age,
                user_gender=user_gender,
                user_id="0001" # for testing only
            )

            output_file = FILES_DIR / f"{gpx_file.stem}.json"
            with open(output_file, "w") as file:
                json.dump(
                    result,
                    file,
                    indent=2,
                    default=str
                )
            print(f"Criado: {output_file.name}\n")
        except Exception as error:
            print(f"Erro em {gpx_file.name}: {error}\n")


def main():
    print("\n=== GPX Processor ===\n")
    print("\nIniciando processamento...\n")

    process_all_gpx_files(
        max_hr=user_max_hr,
        user_weight=user_weight,
        user_age=user_age,
        user_gender=user_gender
    )


if __name__ == "__main__":
    main()