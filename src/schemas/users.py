from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str

    class Config:
        from_attributes = True
