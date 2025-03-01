from fastapi import Depends, HTTPException, status

from config.auth import auth, Hasher
from repositories.users import UserRepository
from schemas.auth import RegisterSchema, LoginSchema
from schemas.token import TokenSchema
from schemas.users import UserCreateSchema


class AuthService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo
        self.__hasher = Hasher()

    async def register(self, payload: RegisterSchema):
        user = await self.repo.get(email=payload.email)
        if user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='User already exists')

        new_user = await self.repo.create(
            payload=UserCreateSchema(email=payload.email, password=self.__hasher.hash_password(payload.password))
        )

        return new_user

    async def login(self, payload: LoginSchema) -> TokenSchema:
        user = await self.repo.get(email=payload.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid email')

        if not self.__hasher.verify_password(password=payload.password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid password')

        token = auth.create_access_token(uid=str(user.id), data={"email": user.email})
        return TokenSchema(access_token=token, type='bearer')
