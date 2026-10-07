from dataclasses import dataclass
from typing import Any


@dataclass
class Activity:
    user_id: str

    start_lat: float
    start_lon: float

    distance_km: float
    duration_sec: float

    elevation_gain: float
    elevation_loss: float

    max_elevation: float
    min_elevation: float

    avg_speed: float
    max_speed: float

    avg_hr: float | None
    max_hr_recorded: float | None

    moving_time_sec: float
    stopped_time_sec: float

    calories: float
    training_load: float
    score: float

    zone_distribution: Any
    zone_percentage: Any
    hr_zones_time: Any

    route: list
    best_efforts: Any
    segment_efforts: list