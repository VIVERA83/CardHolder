from typing import TYPE_CHECKING

from store.database.database import Database

if TYPE_CHECKING:
    from app.core.app import Application


def setup_store(app: "Application"):
    app.db = Database(app)
    app.on_event("startup")(app.db.connect)
    app.on_event("shutdown")(app.db.disconnect)
