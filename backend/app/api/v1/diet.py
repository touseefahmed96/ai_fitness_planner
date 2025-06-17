from app.core.config import Config
from app.db.session import get_db
from app.models.diet import DietPlan
from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from sqlalchemy.orm import Session

router = APIRouter()

# Initialize Groq client
client = Groq(api_key=Config.GROQ_API_KEY)


@router.post("/generate")
def generate_diet_plan(
    user_id: int, calories: int, preferences: str = None, db: Session = Depends(get_db)
):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a {calories}-calorie diet plan with {preferences if preferences else 'no restrictions'}.",
                }
            ],
            model=Config.GROQ_MODEL,
            stream=False,
        )

        diet_plan = chat_completion.choices[0].message.content

        new_plan = DietPlan(user_id=user_id, plan=diet_plan)
        db.add(new_plan)
        db.commit()

        return {"diet_plan": diet_plan}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API error: {str(e)}")
