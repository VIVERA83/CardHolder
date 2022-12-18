from typing import TYPE_CHECKING
from logging import getLogger

if TYPE_CHECKING:
    from core.app import Application


class BaseAccessor:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("accessor")
        app.on_event("startup")(self.connect)
        app.on_event("shutdown")(self.disconnect)

    async def connect(self):
        return

    async def disconnect(self):
        return
