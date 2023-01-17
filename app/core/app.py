from card.routes import setup_routes
from core.helpers import Application
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.settings import Settings
from store import setup_store

app = Application()


def setup_app() -> "Application":
    app.settings = Settings()
    setup_logging(app)
    setup_middleware(app)
    setup_routes(app)
    setup_store(app)
    return app
