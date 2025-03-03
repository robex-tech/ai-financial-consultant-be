from fastapi import APIRouter, status
from fastapi.params import Depends

from api.dependencies.user import token_dependency, CurrentUser
from schemas.users import ChangePasswordSchema
from services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[token_dependency]
)


@router.get('/me')
async def get_user_profile(current_user: CurrentUser):
    return current_user


@router.post(
    '/change-password',
    status_code=status.HTTP_200_OK
)
async def change_password(
        payload: ChangePasswordSchema,
        current_user: CurrentUser,
        user_service: UserService = Depends()
):
    return await user_service.change_password(user_id=current_user.id, payload=payload)
