from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings
from documents.users import User
from documents.dialogs import Dialog


async def init_db():
    client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    await init_beanie(database=client.get_database(settings.db_name), document_models=[User, Dialog])

