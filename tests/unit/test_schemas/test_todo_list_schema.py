from unittest.mock import AsyncMock

import pytest

from src.core.exceptions import NotFound
from tests.utility import AsyncTestClient, get_authentication


@pytest.mark.asyncio
async def test_add(test_client: AsyncTestClient, mock_todo_list_service: AsyncMock) -> None:
    actual = await test_client.put("/api/v1/", json={"name": "test", "description": "test"}, auth=get_authentication())

    assert actual.status_code == 200


@pytest.mark.asyncio
async def test_delete(test_client: AsyncTestClient, mock_todo_list_service: AsyncMock) -> None:
    actual = await test_client.delete("/api/v1/", params={"name": "test"}, auth=get_authentication())

    assert actual.status_code == 200


@pytest.mark.asyncio
async def test_delete_return_400(test_client: AsyncTestClient, mock_todo_list_service: AsyncMock) -> None:
    mock_todo_list_service.return_value.delete.side_effect = NotFound()

    actual = await test_client.delete("/api/v1/", params={"name": "test"}, auth=get_authentication())

    assert actual.status_code == 404


@pytest.mark.asyncio
async def test_list(test_client: AsyncTestClient, mock_todo_list_service: AsyncMock) -> None:
    mock_todo_list_service.return_value.list.return_value = []

    actual = await test_client.get("/api/v1/list/", auth=get_authentication())

    assert actual.status_code == 200
    assert actual.json() == {"items": []}
