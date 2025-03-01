from typing import Annotated

from fastapi import APIRouter, Depends, Form

from schemas.auth import LoginSchema, RegisterSchema
from schemas.token import TokenSchema
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login', response_model=TokenSchema, status_code=201)
async def login(payload: Annotated[LoginSchema, Form()], auth_service: AuthService = Depends()):
    return await auth_service.login(payload)


@router.post('/register', status_code=201)
async def register(payload: RegisterSchema, auth_service: AuthService = Depends()):
    return await auth_service.register(payload)
