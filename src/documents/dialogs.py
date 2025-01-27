from typing import List

from beanie import Document
from pydantic import BaseModel


class Message(BaseModel):
    question: str
    answer: str


class Dialog(Document):
    user_id: str
    messages: List[Message]

    class Settings:
        name = "dialogs"
