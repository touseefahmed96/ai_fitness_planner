from app.core.config import Config
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.diet import DietPlan
from app.models.user import User
from app.schemas.diet import DietRequest, DietResponse
from app.services.groq_client import get_groq_client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/generate", response_model=DietResponse)
def generate_diet_plan(
    request: DietRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        client = get_groq_client()
        preferences = request.preferences or "no restrictions"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a {request.calories}-calorie diet plan with {preferences}.",
                }
            ],
            model=Config.GROQ_MODEL,
            stream=False,
        )

        diet_plan = chat_completion.choices[0].message.content
        new_plan = DietPlan(user_id=current_user.id, plan=diet_plan)
        db.add(new_plan)
        db.commit()

        return {"diet_plan": diet_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API error: {str(e)}")
