from fastapi import FastAPI

app = FastAPI(title="AI Workout & Diet Planner", version="1.0")


@app.get("/")
def home():
    return {"message": "Welcome to the AI Fitness Planner!"}
