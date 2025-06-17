from pydantic import BaseModel


class WorkoutRequest(BaseModel):
    user_id: int
    fitness_level: str
    goal: str


class WorkoutResponse(BaseModel):
    workout_plan: str
