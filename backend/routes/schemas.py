from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    weight: float
    height: float
    goal: str


class UserLogin(BaseModel):
    email: str
    password: str


class WorkoutRequest(BaseModel):
    user_id: int
    fitness_level: str
    goal: str


class DietRequest(BaseModel):
    user_id: int
    calories: int
    preferences: Optional[str] = None


class WorkoutResponse(BaseModel):
    workout_plan: str


class DietResponse(BaseModel):
    diet_plan: str
