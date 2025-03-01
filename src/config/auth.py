from authx import AuthXConfig, AuthX
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)


class Hasher:
    def __init__(self):
        self._pwd_context = pwd_context

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(password, hashed_password)
