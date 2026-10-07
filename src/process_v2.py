
import logging
from typing import Optional, Dict, Any

from src.services.gpx_parser import parse_gpx
from src.services.activity_date import get_activity_start, get_activity_end
from src.services.metrics import (
    calculate_distance,
    calculate_duration,
    calculate_elevation_gain,
    calculate_elevation_loss,
    calculate_max_elevation,
    calculate_min_elevation,
    calculate_max_speed,
    calculate_avg_speed,
)
from src.services.hr_metrics import calculate_avg_hr, calculate_max_hr
from src.services.zones import create_zones, calculate_zone_distribution, calculate_hr_zones_time, zone_percentages
from src.services.movement import calculate_moving_time, calculate_stopped_time
from src.services.calories import estimate_calories
from src.services.training_load import calculate_training_load
from src.services.activity_score import calculate_activity_score
from src.services.route import simplify_route
from src.services.best_efforts import calculate_best_efforts
from src.services.segment_efforts import calculate_segment_efforts

logger = logging.getLogger(__name__)


def _safe_calculate(func, default, error_msg: str, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"{error_msg}: {e}")
        return default


def process_gpx_file(
        content: bytes,
        user_id: str,
        max_hr: int = 210,
        user_weight: Optional[float] = None,
        user_age: Optional[float] = None,
        user_gender: Optional[str] = None,
) -> Dict[str, Any]:

    logger.info(f"Iniciando processamento de GPX para usuário: {user_id}")

    # 1. Parse e Validação Crítica (Estes devem levantar exceção se falharem)
    try:
        points = parse_gpx(content)
    except Exception as e:
        logger.error(f"Erro crítico ao parsear GPX: {e}", exc_info=True)
        raise ValueError(f"Falha ao parsear GPX: {str(e)}")

    if len(points) < 2:
        logger.warning(f"Arquivo GPX inválido com {len(points)} pontos.")
        raise ValueError("Arquivo GPX deve ter no mínimo 2 pontos de rastreamento.")

    # 2. Extração de Datas e Métricas Base
    start_date = _safe_calculate(get_activity_start, None, "Erro ao calcular data inicial", points)
    end_date = _safe_calculate(get_activity_end, None, "Erro ao calcular data final", points)

    distance = _safe_calculate(calculate_distance, 0.0, "Erro ao calcular distância", points)
    duration = _safe_calculate(calculate_duration, 0.0, "Erro ao calcular duração", points)
    elevation_gain = _safe_calculate(calculate_elevation_gain, 0.0, "Erro ao calcular ganho de elevação", points)
    elevation_loss = _safe_calculate(calculate_elevation_loss, 0.0, "Erro ao calcular perda de elevação", points)
    max_elevation = _safe_calculate(calculate_max_elevation, 0.0, "Erro ao calcular elevação máxima", points)
    min_elevation = _safe_calculate(calculate_min_elevation, 0.0, "Erro ao calcular elevação mínima", points)

    avg_speed = calculate_avg_speed(distance, duration)
    max_speed = _safe_calculate(calculate_max_speed, 0.0, "Erro ao calcular velocidade máxima", points)

    # 3. Métricas de Frequência Cardíaca e Zonas
    avg_hr = _safe_calculate(calculate_avg_hr, 0.0, "Erro ao calcular FC média", points)
    recorded_max_hr = _safe_calculate(calculate_max_hr, 0.0, "Erro ao calcular FC máxima", points)

    zones = _safe_calculate(create_zones, None, "Erro ao criar zonas", max_hr)
    zone_dist = _safe_calculate(calculate_zone_distribution, None, "Erro ao calcular distribuição de zonas", points,zones) if zones else None
    zone_pct = _safe_calculate(zone_percentages, None, "Erro ao calcular percentual de zonas", zone_dist) if zone_dist else None
    hr_zones_time = _safe_calculate(calculate_hr_zones_time, None, "Erro ao calcular tempo nas zonas de FC", points,zones) if zones else None

    # 4. Movimento, Carga e Performance
    moving_time = _safe_calculate(calculate_moving_time, duration, "Erro ao calcular tempo em movimento", points)
    stopped_time = calculate_stopped_time(duration, moving_time)

    calories = _safe_calculate(
        estimate_calories, 0.0, "Erro ao estimar calorias",
        avg_hr, moving_time, user_weight, user_age, max_hr, user_gender
    )
    training_load = _safe_calculate(calculate_training_load, 0.0, "Erro ao calcular carga de treino", avg_hr,moving_time, max_hr)
    score = _safe_calculate(calculate_activity_score, 0.0, "Erro ao calcular activity score", distance, elevation_gain,moving_time, hr_zones_time)

    best_efforts = _safe_calculate(calculate_best_efforts, None, "Erro ao calcular best efforts", points)
    segment_efforts = _safe_calculate(calculate_segment_efforts, [], "Erro ao calcular segment efforts", points)
    simplified_route = _safe_calculate(simplify_route, [], "Erro ao simplificar rota", points)

    # 5. Montagem do Resultado
    activity = {
        "user_id": user_id,
        "start_lat": points[0].get("lat"),
        "start_lon": points[0].get("lon"),
        "distance_km": distance,
        "duration_sec": duration,
        "elevation_gain": elevation_gain,
        "elevation_loss": elevation_loss,
        "max_elevation": max_elevation,
        "min_elevation": min_elevation,
        "start_date": start_date,
        "end_date": end_date,
        "avg_speed": avg_speed,
        "max_speed": max_speed,
        "avg_hr": avg_hr,
        "max_hr_recorded": recorded_max_hr,
        "user_max_hr": max_hr,
        "moving_time_sec": moving_time,
        "stopped_time_sec": stopped_time,
        "calories": calories,
        "training_load": training_load,
        "score": score,
        "zone_distribution": zone_dist,
        "zone_percentage": zone_pct,
        "hr_zones_time": hr_zones_time,
        "route": simplified_route,
        "best_efforts": best_efforts,
        "segment_efforts": segment_efforts,
    }

    logger.info(f"GPX processado com sucesso para usuário {user_id}: {distance:.2f}km")
    return activity