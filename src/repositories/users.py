from documents.users import User
from schemas.users import UserSchema, UserCreateSchema


class UserRepository:
    async def create(self, payload: UserCreateSchema) -> UserSchema:
        new_user = User(email=payload.email, password=payload.password)
        await new_user.create()
        return UserSchema.model_validate(new_user)

    async def get(self, email: str):
        user = await User.find_one(User.email == email)
        return user
