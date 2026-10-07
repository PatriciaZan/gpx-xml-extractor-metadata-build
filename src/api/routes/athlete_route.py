from src.database.heart_rate_zones import get_heart_rate_zones
from src.database.save_heart_rate_zones import save_heart_rate_zones
from src.services.heart_zones.calculate_athlete_zones import calculate_athlete_zones
from src.database.db_users import get_user

from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/athletes",
    tags=["Athletes"]
)


@router.post("/{user_id}/zones")
def calculate_zones(user_id: int):

    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Athlete not found"
        )

    try:
        result = calculate_athlete_zones(
            age=user["age"],
            gender=user["sex"],
            max_hr=user["max_heart_rate"],
            rest_hr=user["rest_heart_rate"],
        )

        save_heart_rate_zones(
            user_id=user_id,
            result=result
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get("/{user_id}/zones")
def get_zones(user_id: int):

    zones = get_heart_rate_zones(user_id)

    if not zones:
        raise HTTPException(
            status_code=404,
            detail="No heart rate zones found for this athlete"
        )

    return {
        "user_id": user_id,
        "zones": zones
    }