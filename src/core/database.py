from typing import AsyncGenerator

from beanie import init_beanie
from motor.core import AgnosticClient, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.settings import Application
from src.models.orm import __orm_models__


async def get_database_client(
    settings: Application,
) -> AsyncGenerator[AgnosticClient, None]:  # type: ignore
    client = AsyncIOMotorClient(  # type: ignore
        settings.mongodb.uri,
        maxPoolSize=settings.mongodb.max_pool_size,
        minPoolSize=settings.mongodb.min_pool_size,
    )
    database: AgnosticDatabase = client.get_database()  # type: ignore
    await init_beanie(database=database, document_models=__orm_models__)  # type: ignore[arg-type]
    yield client
    client.close()
