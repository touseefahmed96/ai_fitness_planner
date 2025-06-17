from typing import Optional

from pydantic import BaseModel


class DietRequest(BaseModel):
    user_id: int
    calories: int
    preferences: Optional[str] = None


class DietResponse(BaseModel):
    diet_plan: str
