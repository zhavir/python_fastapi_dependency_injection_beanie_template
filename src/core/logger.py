import logging
import sys
from typing import Generator

import structlog

from src.core.settings import Application


class Logger(structlog.stdlib.BoundLogger):
    pass


def configure_logger(settings: Application) -> Logger:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=settings.logger.log_level.name)
    structlog.configure(
        processors=[
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=Logger,
        cache_logger_on_first_use=True,
    )
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.ExtraAdder(),
            structlog.stdlib.add_logger_name,
            timestamper,
        ],
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            timestamper,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.format_exc_info,
            structlog.processors.EventRenamer("msg"),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.logger.json_format else structlog.dev.ConsoleRenderer(),  # type: ignore
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(settings.logger.log_level.name)
    app_logger: Logger = structlog.get_logger("ToDo")
    app_logger.info("Log level set to", logger_level=settings.logger.log_level.name)
    return app_logger


def get_logger(settings: Application) -> Generator[Logger, None, None]:
    """Get structlog logger client"""
    logger = configure_logger(settings=settings)

    yield logger
