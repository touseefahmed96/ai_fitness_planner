from typing import Optional

from app.core.config import Config
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.diet import DietPlan
from app.models.user import User
from app.schemas.diet import DietRequest, DietResponse
from app.services.groq_client import get_groq_client
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter()


def build_diet_prompt(
    calories: int,
    preferences: Optional[str] = None,
    goal: Optional[str] = None,
    meals_per_day: int = 3,
) -> str:
    base_prompt = f"""Generate a detailed {calories}-calorie daily diet plan.
    
Requirements:
- Total daily calories: {calories}
- Number of meals: {meals_per_day}
- Include macronutrient breakdown (protein, carbs, fats)
- Provide portion sizes and preparation methods
- Include healthy snack options"""

    if preferences:
        base_prompt += f"\n- Dietary preferences/restrictions: {preferences}"

    if goal:
        base_prompt += f"\n- Fitness goal: {goal}"

    base_prompt += """\n
Format the response as a structured daily meal plan with:
1. Breakfast, Lunch, Dinner (and snacks if applicable)
2. Calorie count per meal
3. Brief nutritional benefits
4. Simple preparation instructions"""

    return base_prompt


@router.post("/generate", response_model=DietResponse)
def generate_diet_plan(
    request: DietRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if request.calories < 1000 or request.calories > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Calories must be between 1000 and 5000",
            )

        client = get_groq_client()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service temporarily unavailable",
            )

        prompt = build_diet_prompt(
            calories=request.calories,
            preferences=request.preferences,
            goal=getattr(request, "goal", None),
            meals_per_day=getattr(request, "meals_per_day", 3),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a certified nutritionist and dietitian. Create practical, healthy, and balanced meal plans.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=Config.GROQ_MODEL,
            stream=False,
            temperature=0.7,
            max_tokens=2000,
        )

        if not chat_completion.choices:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate diet plan",
            )

        diet_plan_content = chat_completion.choices[0].message.content

        if not diet_plan_content or len(diet_plan_content.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Generated diet plan is too short or empty",
            )

        # Save to database with error handling
        try:
            new_plan = DietPlan(
                user_id=current_user.id,
                plan=diet_plan_content,
                calories=request.calories,
                preferences=request.preferences,
            )
            db.add(new_plan)
            db.commit()
            db.refresh(new_plan)

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save diet plan",
            )

        return DietResponse(
            diet_plan=diet_plan_content,
            calories=request.calories,
            plan_id=new_plan.id,
            created_at=new_plan.created_at,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating your diet plan",
        )
