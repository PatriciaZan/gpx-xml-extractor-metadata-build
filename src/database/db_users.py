from src.database.connection import get_connection

def get_user(user_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    age,
                    sex,
                    height,
                    weight,
                    max_heart_rate,
                    rest_heart_rate
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "sex": row[3],
                "height": row[4],
                "weight": row[5],
                "max_heart_rate": row[6],
                "rest_heart_rate": row[7],
            }