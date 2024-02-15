from abc import ABC, abstractmethod

from src.core.logger import Logger


class BaseService(ABC):
    @abstractmethod
    def __init__(self, logger: Logger) -> None:
        self._logger = logger
