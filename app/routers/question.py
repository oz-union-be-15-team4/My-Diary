from http.client import HTTPException

from fastapi import APIRouter, Depends
import random

from app.models.question import Question
from app.schemas.question import QuestionRead


router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/random", response_model=QuestionRead)
async def get_random_question() -> QuestionRead:
    questions = await Question.all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions available")

    question = random.choice(questions)

    return question