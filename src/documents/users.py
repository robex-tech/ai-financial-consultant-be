from datetime import datetime

from beanie import Document
from pydantic import Field


class User(Document):
    email: str
    password: str
    joined_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'users'
