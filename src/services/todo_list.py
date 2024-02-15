from typing import List

from src.core.logger import Logger
from src.models.domain.todo_list import TodDoListItemDomain
from src.repositories.todo_list import ToDoListRepository
from src.services.base import BaseService


class ToDoListService(BaseService):
    def __init__(
        self,
        todo_list_repository: ToDoListRepository,
        logger: Logger,
    ) -> None:
        super().__init__(logger)
        self.todo_list_repository = todo_list_repository

    async def list(self) -> List[TodDoListItemDomain]:
        await self._logger.ainfo("received list request")
        return await self.todo_list_repository.list()

    async def delete(self, name: str) -> None:
        await self._logger.ainfo("received delete request for", name=name)
        await self.todo_list_repository.delete(name=name)

    async def add(self, data: TodDoListItemDomain) -> None:
        await self._logger.ainfo("received add request for", data=data)
        await self.todo_list_repository.add(data=data)
