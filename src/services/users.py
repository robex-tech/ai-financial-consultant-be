from fastapi import HTTPException
from fastapi.params import Depends

from repositories.users import UserRepository


class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    async def get(self, email: str):
        user = await self.repo.get(email)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user
