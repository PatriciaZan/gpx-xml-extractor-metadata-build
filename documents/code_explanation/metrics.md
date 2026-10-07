# scr/services/metrics.py

Este arquivo contém funções para calcular métricas de um trajeto/percurso (como um passeio de bicicleta, trilha ou rota). Ele trabalha com pontos de GPS que têm latitude, longitude, elevação e timestamp.
- ✅ Distância total percorrida
- ✅ Tempo gasto
- ✅ Subidas e descidas
- ✅ Altitudes máxima/mínima
- ✅ Velocidades máxima e média

## Funções principais:
### 1. `haversine(lat1, lon1, lat2, lon2)`  
Calcula a distância em km entre dois pontos de GPS usando a fórmula de Haversine.

- Usa o raio da Terra (6371 km)
- Converte graus para radianos
- Retorna a distância em km


###  2. `calculate_distance(points)`  

Soma a distância entre todos os pontos consecutivos do trajeto.

- Itera por cada ponto
- Usa haversine() para calcular distância entre pares
- Retorna a distância total em km (arredondada)

### `3. calculate_duration(points)`  
Calcula o tempo total do trajeto.

- Pega o primeiro e último ponto
- Retorna a diferença em segundos

### `4. calculate_elevation_gain(points)`  
Calcula o total de metros subidos.

- Compara elevações consecutivas
- Soma apenas quando a elevação aumenta
- Ignora valores None (pontos sem altitude)

### `5. calculate_elevation_loss(points)`  
Calcula o total de metros descidos.

- Semelhante ao anterior, mas soma apenas descidas
- Usa abs() para converter negativo em positivo

### `6. calculate_max_elevation(points)` e `calculate_min_elevation(points)`  
Encontram a maior e menor altitude do trajeto.

- Filtram valores None
- Retornam None se não houver dados de elevação

### `7. calculate_max_speed(points)`  
Calcula a velocidade máxima registrada entre pontos consecutivos.

- Usa a distância e tempo entre pontos
- Converte para km/h
- Retorna o maior valor encontrado

### `8. calculate_avg_speed(distance_km, duration_sec)`  
Calcula a velocidade média do trajeto.

- Fórmula: velocidade = distância / tempo
- Retorna em km/h

## Estrutura esperada dos dados:
Os `points` devem ser uma lista de dicionários assim:
```python
    points = [
        {"lat": -23.5505, "lon": -46.6333, "elevation": 800, "time": datetime(...)},
        {"lat": -23.5510, "lon": -46.6340, "elevation": 815, "time": datetime(...)},
        # ... mais pontos
    ]
```