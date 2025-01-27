from fastapi import FastAPI

from config.auth import auth
from config.database import init_db
from routers.users import router as users_router
from routers.auth import router as auth_router

app = FastAPI()

auth.handle_errors(app)


@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(users_router)
app.include_router(auth_router)
