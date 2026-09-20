# GPX-XML Data Extractor & Cycling Metadata Constructor
**Personal Experimenting project, very raw and crude code.**   
---
A Python-based backend application designed to ingest, parse, and extract deep analytical metadata from cycling GPX/XML activity files. It processes complex physiological and geographical metrics, calculates performance scores, and seamlessly persists data to Supabase while exposing functionality via a structured API.


## 🚀 Features

- **Advanced GPX/XML Parsing**: High-performance extraction of raw geographic coordinates, timestamps, and sensor data from activity files.
- **Cycling Metrics & Analytics**: Computes comprehensive performance indicators including:
  - Movement, route, and elevation metrics (`movement.py`, `route.py`, `metrics.py`)
  - Heart rate metrics and training zones (`hr_metrics.py`, `zones.py`)
  - Training load, segment efforts, and best efforts (`training_load.py`, `segment_efforts.py`, `best_efforts.py`)
  - Calorie expenditure and algorithmic activity scoring (`calories.py`, `activity_score.py`)
- **Database Persistence**: Integrated with Supabase via a clean repository pattern for efficient storage and retrieval of historical ride data (`supabase_client.py`, `activity_repository.py`).
- **API Integration**: Initialized API layer (`api/api_app.py`) for handling activity uploads and data queries.


## 🛠️ Project Structure

```text
GPX-XML-Data-Extractor/
├── .env.exemple          # Environment template
├── requirements.txt      # Project dependencies
├── ROADMAP.md            # Project milestones and future plans
├── files/                # Sample files and outputs (e.g., Morning_Ride_result.json)
└── src/
    ├── api/              # API application routes
    │   └── api_app.py
    ├── services/         # Modular processing and metric calculators
    │   ├── activity_date.py
    │   ├── activity_repository.py
    │   ├── activity_score.py
    │   ├── best_efforts.py
    │   ├── calories.py
    │   ├── gpx_parser.py
    │   ├── hr_metrics.py
    │   ├── metrics.py
    │   ├── movement.py
    │   ├── route.py
    │   ├── segment_efforts.py
    │   ├── supabase_client.py
    │   ├── training_load.py
    │   └── zones.py
    ├── gpx_processor.py  # Pipeline orchestration
    └── process_gpx_file.py # Main execution entrypoint
```

## ⚙️ Installation & Setup

1. Clone the repository:
2. Create and activate a virtual environment:
```
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
3. Install dependencies:
```
    pip install -r requirements.txt
```

4. Configure Environment Variables:  
Duplicate .env.exemple as .env and fill in your Supabase credentials and configuration keys:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 💡 Usage
This project can be used from two ways.
1. The most Simple way:
- Download your `.gpx` activity file (works best for cycling)
- Copy in the root folder `/files`
- Execute the file `process_gpx_file.py`
- Complete with your personal data for better result
- A json result file will be added in the `/files` 

2. The second way you will have to configure a supabase DB **DO NOT RECOMENT**
- I don't have the final schema build for the tables
- It works best in my full project with supabase+frontend auth

## 🗺️ Roadmap
Check out the ROADMAP.md file for a complete overview of completed milestones, ongoing advanced cycling analytics implementations, and future production goals.


---

_This project is made by me for study and experimenting , it is an ongoing project and I'm still playing with_