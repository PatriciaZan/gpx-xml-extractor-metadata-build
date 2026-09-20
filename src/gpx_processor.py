"""
Módulo de processamento de arquivos GPX.
Lógica centralizada que pode ser usada pela API ou scripts.
"""
import logging
from typing import Optional, List, Dict, Any

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


def process_gpx_file(
        content: bytes,
        user_id: str,
        max_hr: int = 210,
        user_weight: Optional[float] = None,
        user_age: Optional[float] = None,
        user_gender: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Processa um arquivo GPX e retorna todas as métricas.

    Args:
        content: Bytes do arquivo GPX
        user_id: ID do usuário
        max_hr: Frequência cardíaca máxima do usuário (padrão: 210)
        user_weight: Peso do usuário em kg (opcional)
        user_age: Idade do usuário (opcional)
        user_gender: Gênero do usuário (opcional)

    Returns:
        Dicionário com todas as métricas calculadas

    Raises:
        ValueError: Se o arquivo GPX for inválido ou vazio
    """
    logger.info(f"Iniciando processamento de GPX para usuário: {user_id}")

    # --- Parse ---
    try:
        points = parse_gpx(content)
    except Exception as e:
        logger.error(f"Erro ao parsear GPX: {e}", exc_info=True)
        raise ValueError(f"Falha ao parsear GPX: {str(e)}")

    # Validar quantidade mínima de pontos
    if len(points) < 2:
        logger.warning(f"Arquivo GPX tem {len(points)} pontos (mínimo: 2)")
        raise ValueError("Arquivo GPX deve ter no mínimo 2 pontos de rastreamento")

    # --- Time ---
    try:
        start_date = get_activity_start(points)
        end_date = get_activity_end(points)
    except Exception as e:
        logger.warning(f"Erro ao calcular datas: {e}")
        start_date = None
        end_date = None

    # --- Core metrics ---
    try:
        distance = calculate_distance(points)
        duration = calculate_duration(points)
        elevation_gain = calculate_elevation_gain(points)
        elevation_loss = calculate_elevation_loss(points)
        max_elevation = calculate_max_elevation(points)
        min_elevation = calculate_min_elevation(points)
        avg_speed = calculate_avg_speed(distance, duration)
        max_speed = calculate_max_speed(points)
    except Exception as e:
        logger.error(f"Erro ao calcular métricas core: {e}", exc_info=True)
        distance = 0.0
        duration = 0.0
        elevation_gain = 0.0
        elevation_loss = 0.0
        max_elevation = 0.0
        min_elevation = 0.0
        avg_speed = 0.0
        max_speed = 0.0

    # --- Heart rate ---
    try:
        avg_hr = calculate_avg_hr(points)
        recorded_max_hr = calculate_max_hr(points)
    except Exception as e:
        logger.warning(f"Erro ao calcular frequência cardíaca: {e}")
        avg_hr = 0.0
        recorded_max_hr = 0.0

    # --- Zones (computed once, reused) ---
    try:
        zones = create_zones(max_hr)
        zone_dist = calculate_zone_distribution(points, zones)
        zone_pct = zone_percentages(zone_dist)
        hr_zones_time = calculate_hr_zones_time(points, zones)
    except Exception as e:
        logger.warning(f"Erro ao calcular zonas: {e}")
        zones = None
        zone_dist = None
        zone_pct = None
        hr_zones_time = None

    # --- Movement ---
    try:
        moving_time = calculate_moving_time(points)
        stopped_time = calculate_stopped_time(duration, moving_time)
    except Exception as e:
        logger.warning(f"Erro ao calcular movimento: {e}")
        moving_time = duration
        stopped_time = 0.0

    # --- Load, calories, score ---
    try:
        calories = estimate_calories(avg_hr, moving_time, user_weight, user_age, max_hr, user_gender)
        training_load = calculate_training_load(avg_hr, moving_time, max_hr)
        score = calculate_activity_score(distance, elevation_gain, moving_time, hr_zones_time)
    except Exception as e:
        logger.warning(f"Erro ao calcular calorias/score: {e}")
        calories = 0.0
        training_load = 0.0
        score = 0.0

    # --- Best efforts (fastest window of each target distance) ---
    try:
        best_efforts = calculate_best_efforts(points)
    except Exception as e:
        logger.warning(f"Erro ao calcular best efforts: {e}")
        best_efforts = None

    # --- Segment efforts (sequential 5km splits across the ride) ---
    try:
        segment_efforts = calculate_segment_efforts(points)
    except Exception as e:
        logger.warning(f"Erro ao calcular segment efforts: {e}")
        segment_efforts = []

        # --- Route ---
    try:
        simplified_route = simplify_route(points)
    except Exception as e:
        logger.warning(f"Erro ao simplificar rota: {e}")
        simplified_route = []

    activity = {
        "user_id": user_id,
        "start_lat": points[0]["lat"],
        "start_lon": points[0]["lon"],
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