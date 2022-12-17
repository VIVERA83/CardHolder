import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app import Application


def setup_logging(app: "Application") -> None:
    logging.basicConfig(level=app.settings.logging.level)

