# Project Roadmap: GPX-XML Data Extractor & Cycling  Running Metadata Constructor
For now the cycling works the best


---

## Phase 1: Core Foundation & GPX Parsing (Completed)
Establish the basic file ingestion pipeline and low-level data parsing.
- [x] **Project Structure Setup**: Configure modular directory layout (`src/services`, `src/api`).
- [x] **GPX/XML Parsing**: Implement `gpx_parser.py` to ingest raw XML data points.
- [x] **Basic Metrics & Movement**: Extract foundational tracking details (`movement.py`, `metrics.py`, `route.py`, `activity_date.py`).
- [x] **Pipeline Orchestration**: Build core processing entrypoints (`gpx_processor.py`, `process_gpx_file.py`).

---

## Phase 2: Advanced Cycling Analytics & Metrics (In Progress)
Implement domain-specific cycling algorithms for performance and physiological evaluation.
- [x] **Heart Rate & Zones**: Process HR metrics (`hr_metrics.py`) and training zones (`zones.py`).
- [x] **Effort & Load Analysis**: Calculate training load (`training_load.py`), best efforts (`best_efforts.py`), and segment efforts (`segment_efforts.py`).
- [x] **Energy Expenditure**: Implement calorie computation models (`calories.py`).
- [x] **Activity Scoring**: Develop algorithmic scoring systems for rides (`activity_score.py`).
- [ ] **Power & Elevation Smoothing**: Add advanced smoothing algorithms for noisy GPS altitude and power data.

---

## Phase 3: Storage & API Integration (Next Steps)
Connect the data extraction engine to a backend database and web service layer.
- [x] **Database Client**: Configure Supabase connectivity (`supabase_client.py`).
- [x] **Repository Pattern**: Implement activity data persistence (`activity_repository.py`).
- [x] **API Endpoints**: Initialize API routes (`api/api_app.py`) to handle file uploads and metadata retrieval.
- [ ] **Authentication & Security**: Add API key or user authentication middleware for endpoint protection.
Working with supabase, so some things might change.
- [ ] **Batch Processing**: Enable multi-file ingestion and asynchronous background task processing for bulk uploads.

---

## Phase 4: Testing, Optimization & DX (Future Vision)
Ensure high code reliability, performance optimization, and developer experience.
- [ ] **Unit & Integration Testing**: Write pytest suites for individual metric calculators and API endpoints using sample files (e.g., `Morning_Ride_result.json`).
- [ ] **CI/CD Pipeline**: MUST UNDERSTAND MORE ABOUT THIS
- [ ] **Dockerization**: Containerize the application with a `Dockerfile` and `docker-compose.yml` for seamless deployment.
- [ ] **Export Formats**: Support additional export targets beyond JSON (e.g., CSV, FIT file conversion).