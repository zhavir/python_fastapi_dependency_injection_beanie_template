import pytest

from src.core.container import Container
from src.models.domain.todo_list import TodDoListItemDomain
from src.repositories.todo_list import ToDoListRepository
from tests.utility import AsyncTestClient, get_authentication


@pytest.mark.asyncio
async def test_e2e_todo_list(
    test_client: AsyncTestClient,
    container: Container,
) -> None:
    item = TodDoListItemDomain(name="test", description="description")
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    await todo_list_repository.add(item)

    actual = await test_client.get(
        "/api/v1/list/",
        auth=get_authentication(),
    )

    assert actual.status_code == 200
    assert actual.json() == {"items": [item.model_dump()]}

    await test_client.delete(
        "/api/v1/",
        params={"name": item.name},
        auth=get_authentication(),
    )
