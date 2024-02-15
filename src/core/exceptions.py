from typing import TYPE_CHECKING

from fastapi import Request, status
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from src.utilities.misc import DependencyInjectionFastAPI


class ApplicationBaseException(Exception):
    pass


class NotFound(ApplicationBaseException):
    pass


async def not_found_exception_handler(request: Request, exc: ApplicationBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Item not found"},
    )


def add_exception_handlers(application: "DependencyInjectionFastAPI") -> None:
    application.add_exception_handler(NotFound, not_found_exception_handler)
