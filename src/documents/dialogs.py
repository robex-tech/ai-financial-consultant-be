from datetime import datetime
from typing import List, Optional

from beanie import Document, Update, Replace, before_event
from pydantic import BaseModel, Field


class Message(BaseModel):
    question: str
    answer: str


class Dialog(Document):
    user_id: str
    messages: Optional[List[Message]]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @before_event([Replace, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now()

    class Settings:
        name = "dialogs"
