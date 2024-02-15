from dependency_injector import containers, providers

from src.core.database import get_database_client
from src.core.logger import get_logger
from src.core.settings import Application
from src.repositories.todo_list import ToDoListRepository
from src.services.todo_list import ToDoListService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.routers.v1.endpoints.todo_list",
        ]
    )

    settings = providers.Singleton(Application)

    logger = providers.Resource(get_logger, settings=settings)

    database_client = providers.Resource(get_database_client, settings=settings)

    todo_list_repository = providers.Factory(ToDoListRepository, logger=logger)

    todo_list_service = providers.Factory(ToDoListService, todo_list_repository=todo_list_repository, logger=logger)
