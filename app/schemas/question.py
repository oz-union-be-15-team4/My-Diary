from datetime import datetime
from pydantic import BaseModel, ConfigDict

class QuestionBase(BaseModel):
    question_text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)