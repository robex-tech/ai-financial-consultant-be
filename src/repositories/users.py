from beanie import PydanticObjectId

from documents.users import User
from schemas.users import UserSchema, UserCreateSchema, UserUpdateSchema


class UserRepository:
    async def create(self, payload: UserCreateSchema) -> UserSchema:
        new_user = User(email=payload.email, password=payload.password)
        await new_user.create()
        return UserSchema.model_validate(new_user)

    async def get(self, email: str):
        user = await User.find_one(User.email == email)
        return user

    async def get_by_id(self, user_id: str):
        user = await User.find_one(User.id == PydanticObjectId(user_id))
        return user

    async def update(self, user_id: str, payload: UserUpdateSchema):
        update_user = await User.find_one(
            User.id == PydanticObjectId(user_id)
        ).update(
            {"$set": payload.model_dump(exclude_none=True)}
        )
        return update_user
