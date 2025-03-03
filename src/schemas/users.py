import re
from typing import Optional

from pydantic import BaseModel, model_validator, field_validator


class UserSchema(BaseModel):
    id: str
    email: str

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError('Passwords do not match')
        return self

    @classmethod
    @field_validator("new_password")
    def validate_new_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special symbol")
        return value
