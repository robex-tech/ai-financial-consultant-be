from fastapi import FastAPI

from config.auth import auth
from config.database import init_db

from api.routes import all_routes


app = FastAPI()

auth.handle_errors(app)


@app.on_event("startup")
async def startup_event():
    await init_db()

for route in all_routes:
    app.include_router(route)
