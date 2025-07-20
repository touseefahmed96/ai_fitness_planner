from typing import List, Optional

from app.core.config import Config
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.workout import WorkoutPlan
from app.schemas.workout import WorkoutRequest, WorkoutResponse
from app.services.groq_client import get_groq_client
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter()

VALID_FITNESS_LEVELS = ["beginner", "intermediate", "advanced"]
VALID_GOALS = [
    "weight_loss",
    "muscle_gain",
    "strength",
    "endurance",
    "general_fitness",
    "flexibility",
]


def build_workout_prompt(
    fitness_level: str,
    goal: str,
    duration: Optional[int] = None,
    equipment: Optional[List[str]] = None,
    days_per_week: Optional[int] = None,
    target_muscles: Optional[List[str]] = None,
) -> str:
    base_prompt = f"""Create a detailed {fitness_level} level workout plan for {goal.replace("_", " ")}.
    
Requirements:
- Fitness level: {fitness_level}
- Primary goal: {goal.replace("_", " ")}
- Include warm-up and cool-down routines
- Provide exercise descriptions with proper form instructions
- Include sets, reps, and rest periods
- Add progression tips for improvement"""

    if duration:
        base_prompt += f"\n- Session duration: approximately {duration} minutes"

    if days_per_week:
        base_prompt += f"\n- Training frequency: {days_per_week} days per week"

    if equipment:
        base_prompt += f"\n- Available equipment: {', '.join(equipment)}"
    else:
        base_prompt += "\n- Focus on bodyweight exercises (no equipment required)"

    if target_muscles:
        base_prompt += f"\n- Target muscle groups: {', '.join(target_muscles)}"

    base_prompt += """\n
Format the response as a structured workout plan with:
1. Warm-up routine (5-10 minutes)
2. Main workout exercises with sets/reps/rest
3. Cool-down and stretching (5-10 minutes)
4. Safety tips and proper form notes
5. Weekly progression suggestions

Make it practical and safe for the specified fitness level."""

    return base_prompt


@router.post("/generate", response_model=WorkoutResponse)
def generate_workout_plan(
    request: WorkoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if request.fitness_level.lower() not in VALID_FITNESS_LEVELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fitness level must be one of: {', '.join(VALID_FITNESS_LEVELS)}",
            )

        if request.goal.lower() not in VALID_GOALS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Goal must be one of: {', '.join(VALID_GOALS)}",
            )

        duration = getattr(request, "duration", None)
        if duration and (duration < 10 or duration > 180):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workout duration must be between 10 and 180 minutes",
            )

        days_per_week = getattr(request, "days_per_week", None)
        if days_per_week and (days_per_week < 1 or days_per_week > 7):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days per week must be between 1 and 7",
            )

        client = get_groq_client()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service temporarily unavailable",
            )
        prompt = build_workout_prompt(
            fitness_level=request.fitness_level.lower(),
            goal=request.goal.lower(),
            duration=duration,
            equipment=getattr(request, "equipment", None),
            days_per_week=days_per_week,
            target_muscles=getattr(request, "target_muscles", None),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a certified personal trainer and fitness expert. Create safe, effective, and well-structured workout plans that prioritize proper form and injury prevention.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=Config.GROQ_MODEL,
            stream=False,
            temperature=0.7,
            max_tokens=2500,
        )

        if not chat_completion.choices:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate workout plan",
            )

        workout_plan_content = chat_completion.choices[0].message.content

        if not workout_plan_content or len(workout_plan_content.strip()) < 100:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Generated workout plan is too short or empty",
            )

        try:
            new_plan = WorkoutPlan(
                user_id=current_user.id,
                plan=workout_plan_content,
                fitness_level=request.fitness_level.lower(),
                goal=request.goal.lower(),
                duration=duration,
                days_per_week=days_per_week,
            )
            db.add(new_plan)
            db.commit()
            db.refresh(new_plan)

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save workout plan",
            )

        return WorkoutResponse(
            workout_plan=workout_plan_content,
            fitness_level=request.fitness_level.lower(),
            goal=request.goal.lower(),
            duration=duration,
            plan_id=new_plan.id,
            created_at=new_plan.created_at,
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating your workout plan",
        )


@router.get("/suggestions/{fitness_level}")
def get_workout_suggestions(
    fitness_level: str, current_user: User = Depends(get_current_user)
):
    """Get workout suggestions based on fitness level."""
    if fitness_level.lower() not in VALID_FITNESS_LEVELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fitness level must be one of: {', '.join(VALID_FITNESS_LEVELS)}",
        )

    suggestions = {
        "beginner": {
            "recommended_duration": "20-30 minutes",
            "recommended_frequency": "3-4 days per week",
            "focus_areas": [
                "basic movements",
                "form development",
                "cardiovascular base",
            ],
            "equipment_needed": ["none", "basic bodyweight exercises"],
        },
        "intermediate": {
            "recommended_duration": "30-45 minutes",
            "recommended_frequency": "4-5 days per week",
            "focus_areas": [
                "strength building",
                "muscle isolation",
                "progressive overload",
            ],
            "equipment_needed": ["dumbbells", "resistance bands", "stability ball"],
        },
        "advanced": {
            "recommended_duration": "45-60+ minutes",
            "recommended_frequency": "5-6 days per week",
            "focus_areas": [
                "advanced techniques",
                "periodization",
                "sport-specific training",
            ],
            "equipment_needed": [
                "full gym access",
                "barbells",
                "specialized equipment",
            ],
        },
    }

    return {
        "fitness_level": fitness_level.lower(),
        "suggestions": suggestions[fitness_level.lower()],
        "available_goals": VALID_GOALS,
    }
