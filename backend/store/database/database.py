from logging import getLogger
from typing import TYPE_CHECKING, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from store.database import db

if TYPE_CHECKING:
    from core.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = getLogger("Database")
        self.engine: Optional[AsyncEngine] = None
        self.db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self.db = db
        self.engine = create_async_engine(
            self.app.settings.postgres.dsn, echo=False, future=True
        )
        self.session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.logger.info("Postgres is connected")

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self.engine:
            await self.engine.dispose()
        self.logger.info("Postgres is disconnected")
