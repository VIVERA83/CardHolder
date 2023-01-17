import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app import Application

LOG_FORMAT = "\x1b[33;20m%(levelname)s:     %(name)s: %(asctime)s : %(message)s\x1b[0m"


def setup_logging(app: "Application") -> None:
    logging.basicConfig(level=app.settings.logging.level, format=LOG_FORMAT)
