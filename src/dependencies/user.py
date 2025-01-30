from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer

from config.auth import auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> dict:
    try:
        token_data = await auth.access_token_required(request)
        return token_data
    except Exception as e:
        print(f"Помилка при отриманні токену за допомогою authx: {e}")

    if token:
        try:
            token_data = await auth.decode_access_token(token)
            return token_data
        except Exception as e:
            print(f"Помилка при декодуванні токену OAuth2: {e}")

    return None