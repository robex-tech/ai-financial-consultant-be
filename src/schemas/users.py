from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    email: str

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: str
    password: str
