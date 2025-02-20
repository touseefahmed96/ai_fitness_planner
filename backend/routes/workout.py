from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from sqlalchemy.orm import Session

from backend.config import Config
from backend.database import get_db
from backend.models import WorkoutPlan

router = APIRouter()

client = Groq(api_key=Config.GROQ_API_KEY)


@router.post("/generate")
def generate_workout_plan(
    user_id: int, fitness_level: str, goal: str, db: Session = Depends(get_db)
):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a {fitness_level} level workout plan for {goal}.",
                }
            ],
            model=Config.GROQ_MODEL,
            stream=False,
        )

        workout_plan = chat_completion.choices[0].message.content

        new_plan = WorkoutPlan(user_id=user_id, plan=workout_plan)
        db.add(new_plan)
        db.commit()

        return {"workout_plan": workout_plan}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API error: {str(e)}")
