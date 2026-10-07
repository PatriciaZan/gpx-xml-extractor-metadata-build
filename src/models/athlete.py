from pydantic import BaseModel, Field


class AthleteZonesRequest(BaseModel):
    age: int = Field(gt=0)
    gender: str
    max_hr: int | None = Field(default=None, gt=0)
    rest_hr: int | None = Field(default=None, gt=0)


class HeartRateZone(BaseModel):
    name: str
    min: int
    max: int


class AthleteZonesResponse(BaseModel):
    max_hr_used: int
    rest_hr_used: int
    fcr: int
    zones: dict[str, HeartRateZone]