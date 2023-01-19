from typing import TYPE_CHECKING

from store.database.database import Database

if TYPE_CHECKING:
    from backend.core.app import Application


class Store:
    def __init__(self, app: "Application"):
        from store.card.accessor import CardAccessor  # pylint: disable=C0415

        self.card = CardAccessor(app)


def setup_store(app: "Application"):
    """
    Configuring the connection and disconnection of storages that need to
    start with the application, here we tell the application which
    databases we launch at the start of the application and how to disable them
    """
    app.database = Database(app)
    app.on_event("startup")(app.database.connect)
    app.on_event("shutdown")(app.database.disconnect)
    app.store = Store(app)
