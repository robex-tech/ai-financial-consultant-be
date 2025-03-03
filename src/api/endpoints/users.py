from fastapi import APIRouter

from api.dependencies.user import token_dependency, CurrentUser

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[token_dependency]
)


@router.get('/me')
def get_user_profile(current_user: CurrentUser):
    return current_user
