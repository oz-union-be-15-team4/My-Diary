from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict, StringConstraints
from datetime import datetime

Username = Annotated[str, StringConstraints(min_length=3, max_length=50)]

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    username: Username
    model_config = ConfigDict(extra="forbid")  # 그대로 사용 가능


class UserRead(UserBase):
    id: int
    username: Username
    created_at: datetime | None = None
    updated_at: datetime | None = None
    # Tortoise 객체에서 바로 뽑아 쓰려면 이거만 신경쓰면 됨
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(UserBase):
    password: str
    model_config = ConfigDict(extra="forbid")