from src.services.supabase_client import supabase


def save_activity(activity: dict) -> dict:
    result = (
        supabase
        .table("activities")
        .insert(activity)
        .execute()
    )
    if not result.data:
        raise RuntimeError("Supabase insert returned no data. Activity may not have been saved.")
    return result.data[0]
