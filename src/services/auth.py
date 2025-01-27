from fastapi import Depends, HTTPException
from starlette import status

from config.auth import auth, pwd_context
from repositories.users import UserRepository
from schemas.auth import RegisterSchema, LoginSchema
from schemas.token import TokenSchema


class AuthService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    async def register(self, payload: RegisterSchema):
        user = await self.repo.is_user_exists(email=payload.email)
        if user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='User already exists')

        new_user = await self.repo.create(
            email=payload.email,
            password=self.__hash_password(payload.password)
        )
        return new_user

    async def login(self, payload: LoginSchema) -> TokenSchema:
        user = await self.repo.get(email=payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid email')

        if not self.__verify_password(password=payload.password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid password')

        token = auth.create_access_token(uid=payload.email)
        return TokenSchema(access_token=token)

    @staticmethod
    def __hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def __verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
