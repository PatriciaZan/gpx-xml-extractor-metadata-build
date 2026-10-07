from fastapi import FastAPI

from src.api.routes.athlete_route import router as athlete_router


app = FastAPI(
    title="Athlete Metrics API",
    description="API para cálculo de métricas de atletas.",
    version="1.0.0",
)

app.include_router(athlete_router)