from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import LogLevel


class Router(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="fastapi_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )

    api_prefix: str = "/api"
    api_v1_prefix: str = "/v1"


class Authentication(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env", env_file_encoding="utf-8", extra="ignore")

    username: str = "username"
    password: str = "password"


class Fastapi(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="fastapi_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    router: Router = Router()
    authentication: Authentication = Authentication()


class Uvicorn(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="uvicorn_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = False
    workers: int = 3


class MongoDB(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env", env_file_encoding="utf-8", extra="ignore")

    max_pool_size: int = 10
    min_pool_size: int = 1

    uri: str = "mongodb://root:example@mongodb:27017/test"


class Logger(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="logger_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    json_format: bool = True
    log_level: LogLevel = LogLevel.INFO


class Application(BaseSettings):
    uvicorn: Uvicorn = Uvicorn()
    fastapi: Fastapi = Fastapi()
    mongodb: MongoDB = MongoDB()
    logger: Logger = Logger()


@lru_cache
def get_settings() -> Application:
    return Application()
