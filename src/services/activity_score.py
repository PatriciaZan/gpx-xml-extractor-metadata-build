# Zone intensity weights — each zone's contribution per second is multiplied
# by this factor before being summed. Higher zones are exponentially harder
# to sustain, so they earn disproportionately more points.
ZONE_WEIGHTS = {
    "z1": 0.5,
    "z2": 1.0,
    "z3": 2.0,
    "z4": 3.5,
    "z5": 5.0,
}

def calculate_activity_score(
    distance_km,
    elevation_gain,
    moving_time_sec,
    hr_zones_time,
):
    """
    Score on a 0–100 scale built from three independent pillars:

    1. Intensity  (0–50 pts)
       Weighted zone time as a share of moving time.
       Zone weights: Z1×0.5 / Z2×1.0 / Z3×2.0 / Z4×3.5 / Z5×5.0
       A ride spent entirely in Z5 would score 50; one entirely in Z1 scores 5.
       This makes 100 genuinely hard — you need sustained high-zone effort.

    2. Volume     (0–30 pts)
       10 pts per hour of moving time, capped at 3 h (30 pts).
       Duration matters, but it can't carry the whole score alone.

    3. Terrain    (0–20 pts)
       Elevation gain per km ridden, scaled so 20 m/km → ~20 pts.
       Rewards climbers; flat rides score low here regardless of distance.
    """
    # --- 1. Intensity score ---
    if moving_time_sec > 0 and hr_zones_time:
        weighted_sum = sum(
            hr_zones_time.get(zone, 0) * weight
            for zone, weight in ZONE_WEIGHTS.items()
        )
        # Normalise: if every second were in Z5 (weight 5.0) → raw = 5.0
        # We want that to map to 50 pts, so divide by moving_time and * 10
        raw_intensity = weighted_sum / moving_time_sec   # 0.5 – 5.0 range
        intensity_score = min(raw_intensity * 10, 50)
    else:
        # No HR data — fall back to a modest flat score based on duration only
        intensity_score = 0.0

    # --- 2. Volume score ---
    moving_hours = moving_time_sec / 3600
    volume_score = min(moving_hours * 10, 30)

    # --- 3. Terrain score ---
    if distance_km > 0:
        gain_per_km = elevation_gain / distance_km   # e.g. 20 m/km is hilly
        terrain_score = min(gain_per_km, 20)         # cap at 20 m/km → 20 pts
    else:
        terrain_score = 0.0

    total = intensity_score + volume_score + terrain_score
    return round(min(total, 100))


def score_label(score: int) -> str:
    if score < 20:
        return "Recovery"
    if score < 40:
        return "Easy"
    if score < 60:
        return "Moderate"
    if score < 80:
        return "Hard"
    return "Elite Effort"