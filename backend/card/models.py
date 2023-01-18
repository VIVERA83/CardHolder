import enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from store.database.sqlalchemy_base import db


class StatusCardEnum(enum.Enum):
    not_active: str = "not_active"
    active: str = "active"
    expired: str = "expired"


class DurationEnum(enum.Enum):
    year: datetime = timedelta(days=365)
    six_months: datetime = timedelta(days=180)
    month: datetime = timedelta(days=30)


@dataclass
class CardModel(db):
    __tablename__ = "cards"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    series: int = Column(Integer, primary_key=True)
    number: int = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    create_data: datetime = Column(TIMESTAMP, default=datetime.now())
    expire_date: datetime = Column(
        TIMESTAMP, default=datetime.now() + DurationEnum.month.value
    )
    status: str = Column(Enum(StatusCardEnum), default=StatusCardEnum.not_active)
    card_transactions: list["CardTransactionsModel"] = relationship(
        "CardTransactionsModel",
        backref="cards",
        cascade="all, delete",
        passive_deletes=True,
    )


@dataclass
class CardTransactionsModel(db):
    __tablename__ = "card_transactions"  # noqa

    id: uuid4 = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    transaction_amount: float = Column(Float, nullable=False)
    transaction_date: datetime = Column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    id_card: uuid4 = Column(
        UUID(as_uuid=True), ForeignKey("cards.id", ondelete="CASCADE"), nullable=False
    )
