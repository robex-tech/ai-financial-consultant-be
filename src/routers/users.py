from fastapi import APIRouter
from fastapi.params import Depends

from services.users import UserService

router = APIRouter(prefix='/users')


@router.get('/{email}/')
async def get_user(email: str, service: UserService = Depends()):
    return await service.get(email)
