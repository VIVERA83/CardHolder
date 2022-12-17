import logging
from typing import TYPE_CHECKING, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from core.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self._session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(self.app.settings.postgres.dsn, echo=True, future=True)
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        logging.info("Postgres is connected")

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
        logging.info("Postgres is disconnected")
