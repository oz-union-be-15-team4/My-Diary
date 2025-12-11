from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class DiaryBase(BaseModel):
    title: str
    content: str


class DiaryCreate(DiaryBase):
    created_at: datetime | None = None


class DiaryRead(DiaryBase):
    id: int
    user_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    # 알 수 없는 필드 들어오면 막기
    model_config = ConfigDict(extra="forbid")


class DiaryResponse(DiaryBase):
    id: int
    user_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)