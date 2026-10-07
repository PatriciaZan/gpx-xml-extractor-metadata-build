from dataclasses import dataclass

@dataclass
class UserProfile:
    user_id: str
    max_hr: int = 210
    weight: float | None = None
    age: int | None = None
    gender: str | None = None