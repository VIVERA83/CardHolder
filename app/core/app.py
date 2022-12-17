from fastapi import FastAPI
from typing import Optional
from core.settings import Settings
from core.logger import setup_logging
from store import setup_store


class Application(FastAPI):
    settings: Optional["Settings"] = None


app = Application()


def setup_app() -> "Application":
    app.settings = Settings()
    setup_logging(app)
    setup_store(app)
    return app
