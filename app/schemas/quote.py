from datetime import datetime
from pydantic import BaseModel, ConfigDict

class QuoteBase(BaseModel):
    content: str
    author: str | None = None


class QuoteCreate(QuoteBase):
    pass


class QuoteRead(QuoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)