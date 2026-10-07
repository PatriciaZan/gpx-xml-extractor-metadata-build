from src.database.connection import get_connection


def get_heart_rate_zones(user_id: int) -> list[dict]:

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    zone_code,
                    zone_name,
                    min_hr,
                    max_hr,
                    fcr,
                    max_hr_used,
                    rest_hr_used
                FROM heart_rate_zones
                WHERE user_id = %s
                ORDER BY zone_code
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

            return [
                {
                    "zone_code": row[0],
                    "zone_name": row[1],
                    "min_hr": row[2],
                    "max_hr": row[3],
                    "fcr": row[4],
                    "max_hr_used": row[5],
                    "rest_hr_used": row[6],
                }
                for row in rows
            ]