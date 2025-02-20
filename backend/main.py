from fastapi import FastAPI
from routes import diet, user, workout

app = FastAPI(title="AI Workout & Diet Planner", version="1.0")


# Include routes
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(workout.router, prefix="/workout", tags=["Workout"])
app.include_router(diet.router, prefix="/diet", tags=["Diet"])


@app.get("/")
def home():
    return {"message": "Welcome to the AI Fitness Planner!"}
