from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from documents.users import User


async def init_db():
    client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    await init_beanie(database=client.get_database("fastapi_beanie_db"), document_models=[User])
