from typing import Annotated

from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer

from config.auth import auth
from schemas.users import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> UserSchema:
    try:
        token_data = await auth.access_token_required(request)
        return UserSchema(id=token_data.sub, email=token_data.email)
    except Exception as e:
        print(f"Error getting token using authx: {e}")

    if token:
        try:
            token_data = await auth.decode_access_token(token)
            return UserSchema(id=token_data.sub, email=token_data.email)
        except Exception as e:
            print(f"Error decoding OAuth2 token: {e}")

    return None


token_dependency = Depends(auth.access_token_required)

CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
