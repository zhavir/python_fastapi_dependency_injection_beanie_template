from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.container import Container
from src.models.domain.todo_list import TodDoListItemDomain
from src.models.schemas.todo_list import TodDoListItemSchema, ToDoListSchema
from src.services.todo_list import ToDoListService

router = APIRouter(tags=["tracker"])


@router.get(
    "/list/",
    response_model=ToDoListSchema,
)
@inject
async def list(todo_list_service: ToDoListService = Depends(Provide[Container.todo_list_service])) -> ToDoListSchema:
    items = await todo_list_service.list()
    return ToDoListSchema(items=[TodDoListItemSchema(name=i.name, description=i.description) for i in items])


@router.delete(
    "/",
    response_model=None,
)
@inject
async def delete(name: str, todo_list_service: ToDoListService = Depends(Provide[Container.todo_list_service])) -> None:
    await todo_list_service.delete(name=name)


@router.put(
    "/",
    response_model=None,
)
@inject
async def add(
    data: TodDoListItemSchema, todo_list_service: ToDoListService = Depends(Provide[Container.todo_list_service])
) -> None:
    await todo_list_service.add(data=TodDoListItemDomain(name=data.name, description=data.description))
