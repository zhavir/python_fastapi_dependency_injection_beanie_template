from typing import AsyncGenerator, Tuple

from beanie import init_beanie
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient

from src.core.settings import Application, get_settings
from src.models.orm import __orm_models__


class AsyncTestClient(AsyncClient):
    pass


def get_authentication() -> Tuple[str, str]:
    return (
        get_settings().fastapi.authentication.username,
        get_settings().fastapi.authentication.password,
    )


async def get_mockmongo_database_client(
    settings: Application,
) -> AsyncGenerator[AsyncMongoMockClient, None]:
    client = AsyncMongoMockClient(settings.mongodb.uri)
    await init_beanie(database=client.get_database(), document_models=__orm_models__)  # type: ignore[arg-type]
    yield client
