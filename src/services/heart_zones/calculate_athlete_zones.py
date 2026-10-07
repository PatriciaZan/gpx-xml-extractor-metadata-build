from typing import Optional, Dict, Any, List

DEFAULT_REST_HR = 60

# Nome de cada zona e os limites em % da FCR.
# Há 8 limites para 7 zonas: o limite superior de uma zona é o inferior da próxima.
ZONE_NAMES: List[str] = [
    "Recovery",
    "Aerobic",
    "Tempo",
    "SubThreshold",
    "SuperThreshold",
    "Aerobic Capacity",
    "Anaerobic",
]
ZONE_BOUNDARIES_PCT: List[int] = [50, 60, 70, 80, 90, 95, 100, 110]


def calculate_athlete_zones(
        age: int,
        gender: str,
        max_hr: Optional[int] = None,
        rest_hr: Optional[int] = None
) -> Dict[str, Any]:
    """
    Calcula as 7 zonas cardíacas usando o Método de Karvonen (FCR).
    O mínimo de cada zona é sempre o máximo da zona anterior + 1.
    """
    if age <= 0:
        raise ValueError("Age must be greater than zero.")
    if not gender:
        raise ValueError("Gender is required.")

    if not max_hr or max_hr <= 0:
        max_hr = estimate_max_hr(age, gender)

    if not rest_hr or rest_hr <= 0:
        rest_hr = DEFAULT_REST_HR

    if rest_hr >= max_hr:
        raise ValueError("Resting heart rate must be lower than maximum heart rate.")

    fcr = max_hr - rest_hr

    # Limites em bpm (8 valores)
    boundaries = [_karvonen_bpm(fcr, rest_hr, pct) for pct in ZONE_BOUNDARIES_PCT]

    zones: Dict[str, Dict[str, Any]] = {}
    for i, name in enumerate(ZONE_NAMES):
        min_bpm = boundaries[i] if i == 0 else boundaries[i] + 1
        max_bpm = boundaries[i + 1]
        zones[f"Z{i + 1}"] = {"name": name, "min": min_bpm, "max": max_bpm}

    return {
        "max_hr_used": max_hr,
        "rest_hr_used": rest_hr,
        "fcr": fcr,
        "zones": zones,
    }


def _karvonen_bpm(fcr: int, rest_hr: int, pct: int) -> int:
    """
    bpm = FCR * pct% + FC repouso, com arredondamento half-up em aritmética
    inteira (evita erros de ponto flutuante e o arredondamento "bancário" do round()).
    """
    return (fcr * pct + 50) // 100 + rest_hr


def estimate_max_hr(age: int, gender: str) -> int:
    """Estima a FC máxima por idade e gênero."""
    gender_normalized = gender.strip().upper() if gender else "M"

    if gender_normalized in ("F", "FEMININE", "WOMAN"):
        # Gulati et al.
        return int(round(206 - (0.88 * age)))
    # Tanaka et al.
    return int(round(208 - (0.7 * age)))