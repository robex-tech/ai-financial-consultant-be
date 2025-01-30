from fastapi import Depends, HTTPException
from starlette import status

from config.auth import auth, Hasher
from repositories.users import UserRepository
from schemas.auth import RegisterSchema, LoginSchema
from schemas.token import TokenSchema


class AuthService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo
        self.hasher = Hasher()

    async def register(self, payload: RegisterSchema):
        user = await self.repo.is_user_exists(email=payload.email)
        if user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='User already exists')

        new_user = await self.repo.create(
            email=payload.email,
            password=self.hasher.hash_password(payload.password)
        )
        return new_user

    async def login(self, payload: LoginSchema) -> TokenSchema:
        user = await self.repo.get(email=payload.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid email')

        if not self.hasher.verify_password(password=payload.password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid password')

        token = auth.create_access_token(uid=payload.username)
        return TokenSchema(access_token=token, type='bearer')

