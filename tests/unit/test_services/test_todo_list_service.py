from unittest.mock import AsyncMock

import pytest

from src.core.container import Container
from src.models.domain.todo_list import TodDoListItemDomain
from src.services.todo_list import ToDoListService


@pytest.mark.asyncio
async def test_add(container: Container, mock_todo_list_repository: AsyncMock) -> None:
    item = TodDoListItemDomain(name="test", description="description")
    todo_list_service: ToDoListService = await container.todo_list_service()  # type: ignore
    await todo_list_service.add(item)
    mock_todo_list_repository.return_value.add.assert_called_once_with(data=item)


@pytest.mark.asyncio
async def test_list(container: Container, mock_todo_list_repository: AsyncMock) -> None:
    todo_list_service: ToDoListService = await container.todo_list_service()  # type: ignore
    await todo_list_service.list()
    mock_todo_list_repository.return_value.list.assert_called_once_with()


@pytest.mark.asyncio
async def test_delete(container: Container, mock_todo_list_repository: AsyncMock) -> None:
    todo_list_service: ToDoListService = await container.todo_list_service()  # type: ignore
    await todo_list_service.delete(name="test")
    mock_todo_list_repository.return_value.delete.assert_called_once_with(name="test")
