from abc import ABC, abstractmethod

from src.core.logger import Logger


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, logger: Logger) -> None:
        self._logger = logger
