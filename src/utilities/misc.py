from fastapi import FastAPI

from src.core.container import Container


class DependencyInjectionFastAPI(FastAPI):
    container: Container
