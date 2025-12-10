from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiaryCreate(BaseModel):
    title: str
    content: str

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True