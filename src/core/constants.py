from enum import StrEnum
from typing import Optional


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @classmethod
    def _missing_(cls, value: str) -> Optional[str]:  # type: ignore
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None
