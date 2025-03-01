import re

from pydantic import BaseModel, EmailStr, model_validator, field_validator


class LoginSchema(BaseModel):
    username: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

    @classmethod
    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special symbol")
        return value
