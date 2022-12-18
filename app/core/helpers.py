from typing import Optional
from fastapi import FastAPI, Request as FastAPIRequest
from store.database.database import Database
from core.settings import Settings
from store import Store


class Application(FastAPI):
    settings: Optional["Settings"] = None
    store: Optional["Store"] = None
    database: Optional["Database"] = None


class Request(FastAPIRequest):
    app: Optional["Application"] = None
