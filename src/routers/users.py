from fastapi import APIRouter
from fastapi.params import Depends
from config.auth import auth
from dependencies.user import get_current_user

router = APIRouter(prefix='/users', dependencies=[Depends(auth.access_token_required)])

@router.get('/me')
async def current_user():
    return {
        "message": "Успішно отримано дані користувача",
    }


@router.get('/profile')
def get_profile(payload: dict = Depends(get_current_user)):
    return {
        "id": payload,
    }