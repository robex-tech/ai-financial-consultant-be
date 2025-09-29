from typing import List
from beanie import PydanticObjectId

from documents.users import User
from schemas.users import UserSchema, UserCreateSchema, UserUpdateSchema


class UserRepository:
    async def create(self, payload: UserCreateSchema) -> User:
        new_user = User(email=payload.email, password=payload.password)
        await new_user.create()
        return UserSchema.model_validate(new_user)

    async def list(self, email: str) -> List[User]:
        user = await User.find_one(User.email == email)
        return user

    async def get(self, user_id: str) -> User:
        user = await User.find_one(User.id == PydanticObjectId(user_id))
        return user

    async def update(self, user_id: str, payload: UserUpdateSchema) -> User:
        update_user = await User.find_one(
            User.id == PydanticObjectId(user_id)
        ).update(
            {"$set": payload.model_dump(exclude_none=True)}
        )
        return update_user
