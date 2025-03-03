from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from config.auth import Hasher
from repositories.users import UserRepository
from schemas.users import ChangePasswordSchema, UserUpdateSchema


class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo
        self.__hasher = Hasher()

    async def get(self, email: str):
        user = await self.repo.get(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user

    async def change_password(self, user_id: str, payload: ChangePasswordSchema):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        if not self.__hasher.verify_password(password=payload.old_password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid password')

        await self.repo.update(
            user_id=user_id,
            payload=UserUpdateSchema(
                password=self.__hasher.hash_password(payload.new_password)
            )
        )

        return JSONResponse(
            content={"message": "Password updated successfully"},
            status_code=status.HTTP_200_OK
        )
