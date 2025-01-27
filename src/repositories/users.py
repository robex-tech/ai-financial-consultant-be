from documents.users import User
from schemas.users import UserSchema


class UserRepository:
    async def create(self, email: str, password: str) -> UserSchema:
        new_user = User(email=email, password=password)
        await new_user.insert()
        return UserSchema.model_validate(new_user)

    async def get(self, email: str):
        user = await User.find_one(User.email == email)
        return user

    async def is_user_exists(self, email: str) -> bool:
        user = await self.get(email)
        if not user:
            return True
        return False
