from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DiaryBase(BaseModel):
    title: str
    content: str


class DiaryCreate(DiaryBase):
    user_id: int


class DiaryRead(DiaryBase):
    id: int
    user_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)