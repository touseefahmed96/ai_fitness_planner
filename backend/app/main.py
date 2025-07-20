from contextlib import asynccontextmanager

from app.api.v1 import diet, user, workout
from app.core.config import Config
from app.db.init_db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=Config.PROJECT_NAME,
    version=Config.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    import datetime
    import platform
    import sys

    return {
        "status": "healthy",
        "service": "AI Fitness Planner API",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
        "uptime_check": "OK",
    }


app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(workout.router, prefix="/api/v1/workout", tags=["Workout"])
app.include_router(diet.router, prefix="/api/v1/diet", tags=["Diet"])
