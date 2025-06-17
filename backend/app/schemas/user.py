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
