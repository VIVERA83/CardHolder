from typing import Optional

from fastapi import FastAPI
from fastapi import Request as FastAPIRequest

from core.settings import Settings
from store import Store
from store.database.database import Database


class Application(FastAPI):
    settings: Optional["Settings"] = None
    store: Optional["Store"] = None
    database: Optional["Database"] = None


class Request(FastAPIRequest):
    app: Optional["Application"] = None
