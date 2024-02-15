from typing import List

from beanie.odm.operators.update.general import Set

from src.core.exceptions import NotFound
from src.core.logger import Logger
from src.models.domain.todo_list import TodDoListItemDomain
from src.models.orm.todo_list import ToDoListItemDocument
from src.repositories.base import BaseRepository


class ToDoListRepository(BaseRepository):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)

    async def list(self) -> List[TodDoListItemDomain]:
        return await ToDoListItemDocument.find_all().project(TodDoListItemDomain).to_list()

    async def delete(self, name: str) -> None:
        document = await ToDoListItemDocument.find_one(ToDoListItemDocument.name == name)
        if not document:
            raise NotFound
        await document.delete()

    async def add(self, data: TodDoListItemDomain) -> None:
        await ToDoListItemDocument.find_one(ToDoListItemDocument.name == data.name).upsert(
            Set(data.model_dump(exclude={"name"})),  # type: ignore
            on_insert=ToDoListItemDocument(**data.model_dump()),
        )
