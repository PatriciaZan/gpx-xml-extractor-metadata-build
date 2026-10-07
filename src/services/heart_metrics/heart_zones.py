def calculate_hr_zones_time(hr_points: list, zones: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    """
    Varre os pontos de frequência cardíaca de um arquivo GPX e calcula o tempo
    (em segundos ou minutos) que o atleta passou em cada zona.
    """
    # Inicializa o tempo de cada zona com zero
    zone_times = {zone_key: 0.0 for zone_key in zones.keys()}

    if not hr_points:
        return zone_times

    # Exemplo considerando que cada ponto tem um intervalo de tempo (ou frequência de amostragem)
    # Aqui você adaptará para a lógica de leitura do seu parser GPX
    for hr in hr_points:
        for zone_key, limits in zones.items():
            if limits["min"] <= hr <= limits["max"]:
                zone_times[zone_key] += 1  # Incrementa 1 segundo (ou o delta_t do ponto)
                break

    return zone_times