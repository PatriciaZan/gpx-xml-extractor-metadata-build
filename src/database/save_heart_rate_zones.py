from src.database.connection import get_connection

def save_heart_rate_zones(user_id: int, result: dict):

    fcr = result["fcr"]
    max_hr = result["max_hr_used"]
    rest_hr = result["rest_hr_used"]

    with get_connection() as conn:
        with conn.cursor() as cursor:

            for zone_code, zone in result["zones"].items():

                cursor.execute(
                    """
                    INSERT INTO heart_rate_zones (
                        user_id,
                        zone_code,
                        zone_name,
                        min_hr,
                        max_hr,
                        fcr,
                        max_hr_used,
                        rest_hr_used
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

                    ON CONFLICT (user_id, zone_code)
                    DO UPDATE SET
                        zone_name = EXCLUDED.zone_name,
                        min_hr = EXCLUDED.min_hr,
                        max_hr = EXCLUDED.max_hr,
                        fcr = EXCLUDED.fcr,
                        max_hr_used = EXCLUDED.max_hr_used,
                        rest_hr_used = EXCLUDED.rest_hr_used
                    """,
                    (
                        user_id,
                        zone_code,
                        zone["name"],
                        zone["min"],
                        zone["max"],
                        fcr,
                        max_hr,
                        rest_hr,
                    )
                )

        conn.commit()