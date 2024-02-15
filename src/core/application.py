from functools import lru_cache
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.core.authentication import basic_authentication
from src.core.container import Container
from src.core.exceptions import add_exception_handlers
from src.core.settings import get_settings
from src.routers.v1.routers import router as router_v1
from src.utilities.misc import DependencyInjectionFastAPI


@lru_cache
def get_fastapi_application(
    container: Optional[Container] = None,
) -> DependencyInjectionFastAPI:
    settings = get_settings()

    application = DependencyInjectionFastAPI(
        debug=settings.fastapi.debug,
        docs_url=settings.fastapi.docs_url,
        openapi_prefix=settings.fastapi.openapi_prefix,
        openapi_url=settings.fastapi.openapi_url,
        redoc_url=settings.fastapi.redoc_url,
        title="Todo",
        version="1.0.0",
        description="Todo",
    )
    add_exception_handlers(application)

    if container is None:
        container = Container()
    application.container = container

    api_router = APIRouter(
        prefix=settings.fastapi.router.api_prefix,
        dependencies=[Depends(basic_authentication)],
    )

    api_router.include_router(router_v1, prefix=settings.fastapi.router.api_v1_prefix)

    application.include_router(api_router)

    @application.on_event("startup")
    async def startup_event() -> None:
        result = container.init_resources()
        if result is not None and hasattr(result, "__await__"):
            await result

    @application.on_event("shutdown")
    async def shutdown_event() -> None:
        result = container.shutdown_resources()
        if result is not None and hasattr(result, "__await__"):
            await result

    @application.get("/", include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    return application


application = get_fastapi_application()
