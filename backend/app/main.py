from app.api.v1 import diet, user, workout
from app.core.config import Config
from app.db.init_db import init_db
from fastapi import FastAPI

app = FastAPI(title=Config.PROJECT_NAME, version=Config.VERSION)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Welcome to the AI Fitness Planner API"}


app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(workout.router, prefix="/api/v1/workout", tags=["Workout"])
app.include_router(diet.router, prefix="/api/v1/diet", tags=["Diet"])
