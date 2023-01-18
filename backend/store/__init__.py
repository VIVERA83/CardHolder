from typing import TYPE_CHECKING

from store.database.database import Database

if TYPE_CHECKING:
    from backend.core.app import Application


class Store:
    def __init__(self, app: "Application"):
        from store.card.accessor import CardAccessor

        self.card = CardAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_event("startup")(app.database.connect)
    app.on_event("shutdown")(app.database.disconnect)
    app.store = Store(app)
