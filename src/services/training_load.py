def calculate_training_load(avg_hr, duration_sec, max_hr) -> int:
    if avg_hr is None or max_hr <= 0 or duration_sec <= 0:
        return 0
    intensity = avg_hr / max_hr
    duration_hours = duration_sec / 3600
    return round(intensity * duration_hours * 100)
