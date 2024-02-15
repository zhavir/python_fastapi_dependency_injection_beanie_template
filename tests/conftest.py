import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
from asgi_lifespan import LifespanManager
from dependency_injector import providers
from mongomock_motor import AsyncMongoMockClient

from src.core.application import get_fastapi_application
from src.core.container import Container
from src.repositories.todo_list import ToDoListRepository
from src.services.todo_list import ToDoListService
from tests.utility import AsyncTestClient, get_mockmongo_database_client


@pytest.fixture(scope="module")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()

    yield loop

    loop.close()


@pytest.fixture
async def container() -> AsyncGenerator[Container, None]:
    yield Container()


@pytest.fixture
async def test_client(
    container: Container,
) -> AsyncGenerator[AsyncTestClient, None]:
    app = get_fastapi_application(container=container)
    async with AsyncTestClient(app=app, base_url="http://testserver") as client, LifespanManager(app):
        yield client


@pytest.fixture(autouse=True)
async def reset_database(container: Container) -> AsyncGenerator[None, None]:
    client: AsyncMongoMockClient
    with container.database_client.override(
        providers.Resource(get_mockmongo_database_client, settings=container.settings)
    ) as client:
        await client.init()
        yield
        await client.shutdown()


@pytest.fixture
async def mock_todo_list_repository(
    container: Container,
) -> AsyncGenerator[AsyncMock, None]:
    mocked_repository = AsyncMock(spec=ToDoListRepository)

    with container.todo_list_repository.override(providers.Factory(mocked_repository)):
        yield mocked_repository


@pytest.fixture
async def mock_todo_list_service(
    container: Container,
) -> AsyncGenerator[AsyncMock, None]:
    mocked_service = AsyncMock(spec=ToDoListService)

    with container.todo_list_service.override(providers.Factory(mocked_service)):
        yield mocked_service
