from authx import AuthXConfig, AuthX
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = AuthXConfig(
     JWT_ALGORITHM="HS256",
     JWT_SECRET_KEY="SECRET_KEY",
     JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)
