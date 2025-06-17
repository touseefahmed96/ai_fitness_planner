from app.core.config import Config
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.workout import WorkoutPlan
from app.schemas.workout import WorkoutRequest, WorkoutResponse
from app.services.groq_client import get_groq_client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/generate", response_model=WorkoutResponse)
def generate_workout_plan(
    request: WorkoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        client = get_groq_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a {request.fitness_level} level workout plan for {request.goal}.",
                }
            ],
            model=Config.GROQ_MODEL,
            stream=False,
        )

        workout_plan = chat_completion.choices[0].message.content
        new_plan = WorkoutPlan(user_id=current_user.id, plan=workout_plan)
        db.add(new_plan)
        db.commit()

        return {"workout_plan": workout_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API error: {str(e)}")
