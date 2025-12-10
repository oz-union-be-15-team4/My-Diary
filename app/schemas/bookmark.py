from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BookmarkBase(BaseModel):
    quote_id: int


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkRead(BookmarkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)