from core.helpers import Application
from core.settings import Settings
from core.logger import setup_logging
from store import setup_store
from card.api.routes import setup_routes
from icecream import ic
app = Application()


def setup_app() -> "Application":
    app.settings = Settings()
    setup_logging(app)
    setup_routes(app)
    setup_store(app)
    ic(app.settings.postgres.dsn)
    return app
