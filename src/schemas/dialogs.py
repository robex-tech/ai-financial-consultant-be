from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class MessageSchema(BaseModel):
    question: str
    answer: str


class DialogSchema(BaseModel):
    id: PydanticObjectId
    user_id: str
    messages: Optional[List[MessageSchema]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AskQuestionSchema(BaseModel):
    question: str
