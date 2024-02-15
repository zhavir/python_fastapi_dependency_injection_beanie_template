import uvicorn

from src.core.settings import get_settings


def main() -> None:
    settings = get_settings()

    uvicorn.run(
        "src.core.application:application",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=settings.uvicorn.reload,
        workers=settings.uvicorn.workers,
    )


if __name__ == "__main__":
    main()
