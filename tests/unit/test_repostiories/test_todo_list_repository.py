import pytest

from src.core.container import Container
from src.core.exceptions import NotFound
from src.models.domain.todo_list import TodDoListItemDomain
from src.repositories.todo_list import ToDoListRepository


@pytest.mark.asyncio
async def test_list_none_has_found(container: Container) -> None:
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    res = await todo_list_repository.list()
    assert res == []


@pytest.mark.asyncio
async def test_add(container: Container) -> None:
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    res = await todo_list_repository.add(TodDoListItemDomain(name="test", description="description"))  # type: ignore
    assert res is None


@pytest.mark.asyncio
async def test_delete_raise_exception(container: Container) -> None:
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    with pytest.raises(NotFound):
        await todo_list_repository.delete(name="test")


@pytest.mark.asyncio
async def test_list(container: Container) -> None:
    expected_item = TodDoListItemDomain(name="test", description="description")
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    await todo_list_repository.add(expected_item)

    res = await todo_list_repository.list()

    assert res == [expected_item]


@pytest.mark.asyncio
async def test_delete(container: Container) -> None:
    item = TodDoListItemDomain(name="test", description="description")
    todo_list_repository: ToDoListRepository = container.todo_list_repository()
    await todo_list_repository.add(item)

    res = await todo_list_repository.delete(name=item.name)  # type: ignore

    assert res is None
